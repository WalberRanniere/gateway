FROM python:3.11

WORKDIR /app

# Copia o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt /app/requirements.txt

# Instala as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do código
COPY library/ /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
