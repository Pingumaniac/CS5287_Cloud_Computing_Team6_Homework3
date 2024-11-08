FROM python:3.8-slim

WORKDIR /app
COPY ml_server.py .
COPY requirements_ml_server.txt .
COPY cifar10_resnet20.pt .

RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir flask pillow requests

EXPOSE 5000

CMD ["python", "ml_server.py"]
