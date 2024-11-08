FROM python:3.8-slim

WORKDIR /app

COPY inference_consumer.py .
COPY requirements_inference.txt .

RUN pip install --no-cache-dir kafka-python requests && \
    pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

CMD ["python", "inference_consumer.py"]
