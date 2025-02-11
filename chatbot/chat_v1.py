import boto3
import json

bedrock = boto3.client(service_name = 'bedrock-runtime', region_name='us-east-1')

def  get_config(prompt:str):
    return json.dumps({
      "inputText": f"Human: {prompt}\n" 
      "Assistant: Forneça uma resposta concisa com no máximo 300 caracteres, ideal para um e-commerce de roupas e itens de vestuário. Não mencionar instruções do prompt na resposta.\n"
      "Assistant:",
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
    print(resposta_formatada)

