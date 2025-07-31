# 📚 Minha Biblioteca - Projeto com Gateway REST/REST e REST/SOAP

## 1. Introdução

Este projeto simula uma arquitetura de microsserviços com um **API Gateway** centralizado que orquestra e expõe dados de diferentes serviços internos, utilizando tanto **REST** quanto **SOAP** como backends.

O objetivo principal é demonstrar os seguintes conceitos:

- Criação de uma API Gateway RESTful com `Django Ninja`
- Integração com dois microserviços REST simulando **detalhes** e **preço** de livros
- Consumo de um serviço SOAP por meio de um cliente `zeep`
- Implementação do padrão **HATEOAS** para enriquecer a navegação dos recursos
- Exposição via frontend em **React + Vite**

---

## 2. Funcionamento e Arquitetura

A aplicação é composta pelos seguintes serviços:

| Serviço             | Porta | Descrição                                                                 |
|---------------------|-------|---------------------------------------------------------------------------|
| `gateway`           | 8000  | API principal (Django + NinjaAPI) com endpoints REST e consumo HATEOAS    |
| `service_details`   | 8001  | Microserviço REST que retorna dados detalhados de livros via ISBN         |
| `service_price`     | 8002  | Microserviço REST que retorna o preço de livros via ISBN                  |
| `soap_service`      | 8003  | Serviço SOAP (Spyne) que retorna o preço do livro                         |
| `frontend`          | 5173  | Aplicação React que consome os dados do Gateway via HTTP                  |

### ✨ Requisitos atendidos:

- [x] API Gateway funcional (REST)
- [x] Integração com dois serviços REST
- [x] Integração com um serviço SOAP
- [x] Implementação de HATEOAS nos recursos
- [x] Documentação via Swagger (`/api/docs`)
- [x] Frontend com React (Vite)

---

## 3. Tutorial de Instalação e Execução

### 🔧 Pré-requisitos

- Python 3.11+
- Node.js 18+ e npm/yarn
- Git
- (Opcional) Virtualenv: `python3 -m venv venv`

---

### 📁 Clonando o projeto

```bash
git clone https://github.com/seu-usuario/minha-biblioteca.git
cd minha-biblioteca
```


### 🐍 Backend: Criando ambiente virtual e instalando dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🚀 Subindo os serviços backend

Cada serviço roda em uma porta diferente. Você pode abrir múltiplos terminais ou usar tmux, pm2, ou docker se preferir.

#### 1. Gateway (porta 8000)

```bash
cd library
python3 manage.py migrate
python3 manage.py runserver 8000
```

#### 2. Serviço de detalhes (porta 8001)

```bash
cd ../service_details
python3 manage.py runserver
```

#### 3. Serviço de preços REST (porta 8002)

```bash
cd ../service_price
python3 manage.py runserver
```

#### 4. Serviço SOAP (porta 8003)

⚠️ Necessário Python 3.10 (recomenda-se usar venv específico para isso)

```bash
cd ../soap_service
python3.10 -m venv venv
source venv/bin/activate
pip install spyne
python run.py
```

#### 🌐 Frontend (React com Vite)

```bash
cd ../frontend
npm install
npm run dev
```

Acesse em seu navegador: http://localhost:5173

Pesquise pelo ISBN: 3817172719800

Ou ainda pelo ISBN: 9788533302273

## 🛠️ Extras

Swagger da API Gateway:
http://localhost:8000/api/docs

Exemplo de requisição SOAP via Gateway:
GET http://localhost:8000/api/preco-soap/{isbn}