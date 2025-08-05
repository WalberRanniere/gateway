FROM python:3.11

WORKDIR /app

# Copia o requirements.txt primeiro
COPY requirements.txt /app/requirements.txt

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do código
COPY consumer/ /app

CMD ["python", "consumer.py"]
