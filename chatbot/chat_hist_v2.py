import boto3
import json

bedrock = boto3.client(service_name = 'bedrock-runtime', region_name='us-east-1')

historico = []

def get_hist():
    return "\n".join(historico)

def  get_config(prompt:str):
    prompt_text = (
        f"{get_hist()}\n"
        f"Human: {prompt}\n"
        "Assistant: Forneça uma resposta concisa com no máximo 300 caracteres, ideal para um e-commerce de roupas e itens de vestuário. Não mencionar instruções do prompt na resposta.\n"
        "Assistant:"
    )
    return json.dumps({
                "inputText": prompt_text,
                "textGenerationConfig": {
                "maxTokenCount": 100,
                "stopSequences": [],
                "temperature": 0.7,
                "topP": 0.9
                }
    })
    
print(
  f"Assitente: Olá Sou eu Assistente Virtual. :) \n"
  "Em que posso ajudar hoje?"
)

while True:
    entrada = input("User: ")
    historico.append(f"Human: {entrada}")
    if entrada.lower() == "sair":
        break
    response = bedrock.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=get_config(entrada),
        accept="application/json",
        contentType="application/json"
    )
    resposta = json.loads(response['body'].read().decode('utf-8'))
    outputText = resposta['results'][0].get('outputText', 'Resposta não encontrada')
    resposta_formatada = f"Assistente:\n{outputText}\n"
    historico.append(f"Assitant: {resposta_formatada}")
    print(resposta_formatada)

