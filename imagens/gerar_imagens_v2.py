import boto3
import json
import base64

def get_text_prompt():
    return input("Entre com prompt para gerar imagem (in English): ")

def get_file_name():
    return input("Entre com nome do arquivo (exemplo -> 'figura.png'): ")

client = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")

text_prompt = get_text_prompt()
file_name = get_file_name()

titan_image_config =json.dumps({
    "textToImageParams": {
        "text": text_prompt
    },
    "taskType": "TEXT_IMAGE",
    "imageGenerationConfig": {
        "cfgScale": 10,
        "seed":0,
        "quality": "standard",
        "width": 1024,
        "height": 1024,
        "numberOfImages": 1,
    }
})

response = client.invoke_model(
    body=titan_image_config,
    modelId="amazon.titan-image-generator-v2:0",
    accept="application/json",
    contentType="application/json")

response_body = json.loads(response.get("body").read())
base64_image = response_body.get("images")[0]
base_64_image = base64.b64decode(base64_image)

with open(file_name, "wb") as f:
    f.write(base_64_image)

print(f"Image saved as {file_name}")