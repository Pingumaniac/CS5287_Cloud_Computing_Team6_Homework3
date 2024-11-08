from flask import Flask, request, jsonify
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

# Load the pretrained model
model = torch.hub.load('chenyaofo/pytorch-cifar-models', 'cifar10_resnet20', pretrained=False)

# Load the CIFAR-10 pretrained weights from local file
model_path = "cifar10_resnet20.pt"
if os.path.exists(model_path):
    state_dict = torch.load(model_path, map_location=torch.device('cpu'))
    # Adjust if the state_dict is nested
    if "state_dict" in state_dict:
        state_dict = state_dict["state_dict"]
    model.load_state_dict(state_dict, strict=False)
    print("Model loaded successfully from local checkpoint.")
else:
    print(f"Model file {model_path} not found. Please ensure it's in the directory.")
model.eval()

# CIFAR-10 specific normalization
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.247, 0.243, 0.261])
])

# CIFAR-10 class names
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def decode_image(img_data):
    img_bytes = base64.b64decode(img_data)
    return Image.open(io.BytesIO(img_bytes))

def infer_image(image):
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)
    with torch.no_grad():
        output = model(input_batch)
    predicted_idx = torch.max(output, 1)[1]
    return classes[predicted_idx.item()]

@app.route('/infer', methods=['POST'])
def infer():
    if 'image' not in request.json:
        return jsonify({"error": "No image data provided"}), 400
    try:
        image = decode_image(request.json['image'])
        inferred_value = infer_image(image)
        return jsonify({"InferredValue": inferred_value})
    except Exception as e:
        print(f"Error during inference: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
