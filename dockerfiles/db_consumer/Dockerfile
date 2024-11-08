FROM python:3.8

WORKDIR /app

COPY db_consumer.py .
COPY requirements_db_consumer.txt .

RUN pip install -r requirements_db_consumer.txt

CMD ["python", "db_consumer.py"]
