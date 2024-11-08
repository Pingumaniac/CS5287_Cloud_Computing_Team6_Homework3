from kafka import KafkaConsumer, KafkaProducer
import json
import requests

# Assuming VM2's IP is 192.168.5.235 and VM4's IP is 192.168.5.228
KAFKA_BROKER = "kafka-service:9092"
ML_SERVER = "http://ml-server:5000/infer"


consumer = KafkaConsumer(
    "image_data",
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def infer_image(image_data):
    response = requests.post(ML_SERVER, json={'image': image_data})
    if response.status_code == 200:
        return response.json()['InferredValue']
    else:
        print(f"Error inferring image: {response.text}")
        return None

def consume_images():
    for message in consumer:
        image_data = message.value
        inferred_value = infer_image(image_data['Data'])
        if inferred_value:
            result = {
                "ID": image_data['ID'],
                "GroundTruth": image_data['GroundTruth'],
                "InferredValue": inferred_value
            }
            producer.send("inference_results", value=result)
            producer.flush()
            print(f"Sent inference result for image {image_data['ID']}: {inferred_value}")
        else:
            print(f"Failed to infer image {image_data['ID']}")

if __name__ == "__main__":
    consume_images()
