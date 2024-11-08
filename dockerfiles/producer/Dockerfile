FROM python:3.8
WORKDIR /app
COPY producer.py .
COPY requirements_producer.txt .
RUN pip install --no-cache-dir -r requirements_producer.txt
CMD ["python", "producer.py"]
