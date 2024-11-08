import os
import time
import json
from kafka import KafkaProducer
from PIL import Image
import io
import base64
import uuid
import random
from torchvision import datasets
import numpy as np

# VM-specific settings
KAFKA_BROKER = "kafka-service:9092"
LATENCY_LOG = "latency_vm1.log"  # Log file for VM1

# Load CIFAR-10 dataset
cifar10 = datasets.CIFAR10(root='./data', train=True, download=True)
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# Function to add noise to the image
def add_noise(image):
    img_array = np.array(image)
    mean = 0
    stddev = 1
    noise = np.random.normal(mean, stddev, img_array.shape).astype(np.uint8)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

# Function to encode the image to base64
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Set up Kafka producer with specified API version
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks=1,
    api_version=(7, 5, 1)  # Specify the version as required
)

# Send images to Kafka
for i in range(1000):
    index = random.randint(0, len(cifar10) - 1)
    image, label = cifar10[index]
    
    noisy_image = add_noise(image)
    
    message_id = str(uuid.uuid4())
    message = {
        "ID": message_id,
        "GroundTruth": classes[label],
        "Data": encode_image(noisy_image)
    }
    
    start_time = time.time()
    producer.send("image_data", value=message)
    producer.flush()
    end_time = time.time()

    latency = end_time - start_time
    
    # Log the latency
    with open(LATENCY_LOG, 'a') as log_file:
        log_file.write(f'{latency}\n')
    
    print(f"Sent image {i+1}: {classes[label]}, ID: {message_id}, Latency: {latency}")
    
    time.sleep(1)

producer.close()
