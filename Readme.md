# 📚 Minha Biblioteca - Projeto com Gateway REST/SOAP e Message-Oriented Middleware (MOM)

## 1. Introdução

Este projeto simula uma arquitetura de microsserviços com um **API Gateway** centralizado que orquestra e expõe dados de diferentes serviços internos, utilizando **REST**, **SOAP** e **Mensageria Assíncrona** através de filas de mensagens.

O objetivo principal é demonstrar os seguintes conceitos:

- Criação de uma API Gateway RESTful com `Django Ninja`
- Integração com dois microserviços REST simulando **detalhes** e **preço** de livros
- Consumo de um serviço SOAP por meio de um cliente `zeep`
- **Message-Oriented Middleware (MOM)** com **RabbitMQ** para processamento assíncrono
- **Consumer** que processa mensagens e combina dados de múltiplos serviços
- Implementação do padrão **HATEOAS** para enriquecer a navegação dos recursos
- Exposição via frontend em **React + Vite**

---

## 2. Funcionamento e Arquitetura

A aplicação é composta pelos seguintes serviços:

| Serviço             | Porta | Descrição                                                                 |
|---------------------|-------|---------------------------------------------------------------------------|
| `gateway` (library) | 8000  | API principal (Django + NinjaAPI) com endpoints REST, SOAP e Mensageria   |
| `service_details`   | 8001  | Microserviço REST que retorna dados detalhados de livros via ISBN         |
| `service_price`     | 8002  | Microserviço REST que retorna o preço de livros via ISBN                  |
| `soap_service`      | 8003  | Serviço SOAP (Spyne) que retorna o preço do livro                         |
| `consumer`          | -     | Consumer que processa mensagens da fila e salva livros processados        |
| `rabbitmq`          | 5672/15672 | Message Broker (RabbitMQ) para filas de mensagens               |
| `frontend`          | 5173  | Aplicação React que consome os dados do Gateway via HTTP                  |

### ✨ Fluxo de Mensageria (MOM):

1. **📤 Solicitação**: Gateway publica ISBN na fila `livros` via RabbitMQ
2. **🔄 Processamento**: Consumer consome mensagem e busca dados via REST + SOAP
3. **💾 Persistência**: Consumer envia dados processados de volta ao Gateway para salvar
4. **✅ Verificação**: Cliente pode consultar livros processados e salvos

### ✨ Requisitos atendidos:

- [x] API Gateway funcional (REST)
- [x] Integração com dois serviços REST
- [x] Integração com um serviço SOAP
- [x] **Message-Oriented Middleware (MOM) com RabbitMQ**
- [x] **Consumer assíncrono para processamento de mensagens**
- [x] **Processamento híbrido REST + SOAP via mensageria**
- [x] Implementação de HATEOAS nos recursos
- [x] Documentação via Swagger (`/api/docs`)
- [x] Frontend com React (Vite)

---

## 3. Tutorial de Instalação e Execução

### 🔧 Pré-requisitos

- Docker e Docker Compose
- Python 3.11+
- Node.js 18+ e npm/yarn
- Git

---

### 📁 Clonando o projeto

```bash
git clone https://github.com/seu-usuario/gateway-soap-mom.git
cd gateway-soap-mom
```

### 🐳 Execução com Docker Compose (Recomendado)

```bash
# Sobe todos os serviços (Gateway, Serviços, RabbitMQ, Consumer)
docker-compose up --build

# Para executar em background
docker-compose up -d --build
```

**Serviços disponíveis após inicialização:**
- 🌐 **Gateway API**: http://localhost:8000
- 📖 **Swagger/Docs**: http://localhost:8000/docs
- 🐰 **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- ⚛️ **Frontend React**: http://localhost:5173

### 🔄 Testando o Fluxo de Mensageria

#### Via Swagger (http://localhost:8000/docs):

1. **� Solicitar processamento**:
   - Endpoint: `POST /api/solicitar-processamento`
   - Body: `{"isbn": "9788533302273"}`

2. **✅ Verificar processamento**:
   - Endpoint: `GET /api/livro-processado/{isbn}`
   - Substitua `{isbn}` por: `9788533302273`

#### Via cURL:

```bash
# 1. Solicitar processamento de livro
curl -X POST http://localhost:8000/api/solicitar-processamento \
  -H "Content-Type: application/json" \
  -d '{"isbn": "9788533302273"}'

# 2. Aguardar alguns segundos para o consumer processar...

# 3. Verificar se livro foi processado e salvo
curl http://localhost:8000/api/livro-processado/9788533302273
```

### 📊 Monitoramento

```bash
# Ver logs do consumer em tempo real
docker logs consumer -f

# Ver logs de todos os serviços
docker-compose logs -f

# Status dos containers
docker ps
```

---

### 🐍 Execução Manual (Alternativa)

#### Pré-requisitos adicionais:
- RabbitMQ instalado localmente
- Python 3.10 para o serviço SOAP

#### 1. Backend: Criando ambiente virtual e instalando dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Subindo os serviços backend

##### Gateway (porta 8000)
```bash
cd library
python3 manage.py migrate
python3 manage.py runserver 8000
```

##### Serviço de detalhes (porta 8001)
```bash
cd service_details
python3 manage.py runserver 8001
```

##### Serviço de preços REST (porta 8002)
```bash
cd service_price
python3 manage.py runserver 8002
```

##### Serviço SOAP (porta 8003)
```bash
cd soap_service
python run.py
```

##### Consumer (processamento de mensagens)
```bash
cd consumer
python consumer.py
```
#### 🌐 Frontend (React com Vite)

```bash
cd gateway-client
npm install
npm run dev
```

Acesse em seu navegador: http://localhost:5173

---

## 🛠️ Endpoints e Funcionalidades

### 📋 API Gateway (http://localhost:8000)

#### 🔄 Mensageria (MOM):
- `POST /api/solicitar-processamento` - Solicita processamento assíncrono de livro
- `GET /api/livro-processado/{isbn}` - Verifica livro processado e salvo
- `POST /api/enviar-para-fila` - Envia mensagem diretamente para fila

#### 📚 Livros:
- `GET /api/books` - Lista todos os livros
- `GET /api/books-hateoas` - Lista livros com HATEOAS
- `POST /api/livros/criar/` - Cria livro manualmente
- `GET /api/livro-detalhado/{isbn}` - Dados combinados REST+REST
- `GET /api/livro-detalhado-soap/{isbn}` - Dados combinados REST+SOAP

#### � Preços via SOAP:
- `GET /api/preco-soap/{isbn}` - Consulta preço via serviço SOAP

#### 🏷️ Categorias:
- `GET /api/categories` - Lista categorias
- `GET /api/categories-hateoas` - Lista categorias com HATEOAS

### 📖 Swagger/Documentação:
http://localhost:8000/docs

### 🐰 RabbitMQ Management:
http://localhost:15672 (guest/guest)

---

## 🧪 ISBNs de Teste

Use estes ISBNs para testar os fluxos:

| ISBN | Descrição | Preço |
|------|-----------|-------|
| `9788533302273` | Livro de exemplo 1 | R$ 49,90 |
| `3817172719800` | Livro de exemplo 2 | R$ 59,90 |

---

## 🔧 Arquitetura Técnica

### Message-Oriented Middleware (MOM):
- **Message Broker**: RabbitMQ
- **Fila**: `livros` (durável)
- **Padrão**: Producer-Consumer assíncrono
- **Persistência**: Mensagens duráveis para garantir entrega

### Fluxo de Processamento:
```
Cliente → Gateway → RabbitMQ → Consumer → (REST + SOAP) → Gateway → Database
```

### Tecnologias:
- **Gateway**: Django + Django Ninja
- **Mensageria**: RabbitMQ + pika (Python)
- **Consumer**: Python + httpx
- **SOAP**: Spyne + zeep
- **Frontend**: React + Vite
- **Containerização**: Docker + Docker Compose