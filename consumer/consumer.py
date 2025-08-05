import pika
import json
import httpx
import time
import sys
from zeep import Client

def connect_to_rabbitmq():
    """Tenta conectar ao RabbitMQ com retry"""
    max_attempts = 30
    attempt = 1
    
    while attempt <= max_attempts:
        try:
            print(f"[{attempt}/{max_attempts}] Tentando conectar ao RabbitMQ...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            print("✅ Conectado ao RabbitMQ com sucesso!")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"❌ Falha na conexão. Tentando novamente em 2 segundos...")
            time.sleep(2)
            attempt += 1
    
    print("💥 Não foi possível conectar ao RabbitMQ após todas as tentativas")
    sys.exit(1)

# Conexão com RabbitMQ
connection = connect_to_rabbitmq()
channel = connection.channel()

channel.queue_declare(queue='livros', durable=True)

print("[*] Aguardando mensagens. Para sair, pressione CTRL+C")

def processar_livro(isbn: str):
    try:
        print(f"[→] Processando ISBN: {isbn}")
        
        # 1. Consulta REST com timeout
        print("  📖 Buscando detalhes do livro...")
        res_livro = httpx.get(
            f"http://service_details:8001/api/livros/{isbn}",
            timeout=10.0
        )
        res_livro.raise_for_status()
        livro = res_livro.json()
        
        # Validação dos dados do livro
        if not livro.get("titulo"):
            print(f"[⚠️] Livro {isbn} sem título válido")
            return
            
        print(f"  ✓ Livro encontrado: {livro['titulo']}")

        # 2. Consulta SOAP com timeout
        print("  💰 Buscando preço via SOAP...")
        res_soap = httpx.post(
            "http://soap_service:8003/",
            headers={"Content-Type": "text/xml; charset=utf-8"},
            timeout=10.0,
            data=f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.book">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <soap:get_book_price>
                         <isbn>{isbn}</isbn>
                      </soap:get_book_price>
                   </soapenv:Body>
                </soapenv:Envelope>
            """
        )
        res_soap.raise_for_status()

        # Extração dos dados SOAP com validação
        preco = None
        moeda = None
        
        soap_text = res_soap.text
        if "<preco>" in soap_text and "</preco>" in soap_text:
            try:
                preco = soap_text.split("<preco>")[1].split("</preco>")[0].strip()
                preco = float(preco) if preco else 0.0
            except (ValueError, IndexError):
                print("[⚠️] Erro ao extrair preço do SOAP")
                preco = 0.0
                
        if "<moeda>" in soap_text and "</moeda>" in soap_text:
            try:
                moeda = soap_text.split("<moeda>")[1].split("</moeda>")[0].strip()
            except IndexError:
                print("[⚠️] Erro ao extrair moeda do SOAP")
                moeda = "BRL"
        
        if preco is None or moeda is None:
            print(f"[⚠️] Preço não encontrado para ISBN {isbn}")
            preco = 0.0
            moeda = "BRL"
            
        print(f"  ✓ Preço encontrado: {preco} {moeda}")

        print(f"[✓] Livro processado: {livro['titulo']} - {preco} {moeda}")

        # 3. Envio para o Gateway salvar com timeout
        print("  💾 Salvando no banco...")
        dados_livro = {
            "isbn": isbn,
            "titulo": livro.get("titulo", ""),
            "autor": livro.get("autor", ""),
            "preco": preco,
            "moeda": moeda
        }
        
        salvar_response = httpx.post(
            "http://gateway:8000/api/livros/salvar/",
            json=dados_livro,
            timeout=10.0
        )

        if salvar_response.status_code == 200:
            print("[✓] Livro salvo no banco com sucesso!")
        else:
            print(f"[X] Falha ao salvar no banco (HTTP {salvar_response.status_code}): {salvar_response.text}")

    except httpx.TimeoutException:
        print(f"[X] Timeout ao processar ISBN {isbn}")
    except httpx.HTTPStatusError as e:
        print(f"[X] Erro HTTP ao processar ISBN {isbn}: {e.response.status_code}")
    except Exception as e:
        print(f"[X] Erro inesperado ao processar ISBN {isbn}: {e}")


def callback(ch, method, properties, body):
    mensagem = json.loads(body.decode())
    isbn = mensagem.get("isbn")
    if isbn:
        print(f"[→] Recebido ISBN: {isbn}")
        processar_livro(isbn)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='livros', on_message_callback=callback)

channel.start_consuming()
