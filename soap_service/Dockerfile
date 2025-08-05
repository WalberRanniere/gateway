FROM python:3.10

WORKDIR /app

# Copia o requirements.txt específico do soap_service
COPY soap_service/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o resto do código
COPY soap_service/ /app

CMD ["python", "run.py"]
