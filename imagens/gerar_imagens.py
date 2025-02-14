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

stability_image_config = json.dumps({
    "text_prompts": [
        {
            "text": text_prompt,
        }
    ],
    "height": 512,
    "width": 512,
    "steps": 50,
    "cfg_scale": 10,
    "style_preset": 'photographic',
})

response = client.invoke_model(
    body=stability_image_config,
    modelId="stability.stable-diffusion-xl-v1",
    accept="application/json",
    contentType="application/json")

response_body = json.loads(response.get("body").read())
base64_image = response_body.get("artifacts")[0].get("base64")
base_64_image = base64.b64decode(base64_image)

with open(file_name, "wb") as f:
    f.write(base_64_image)

print(f"Image saved as {file_name}")