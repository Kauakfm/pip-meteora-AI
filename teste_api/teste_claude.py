import boto3
import json

bedrock = boto3.client(service_name = 'bedrock-runtime', region_name='us-east-1')
clude_mode_id = 'amazon.titan-text-express-v1'

claude_config = json.dumps({
    "inputText": "Human: Quais são as melhores opções de sandálias para uma caminhada na praia?\n" 
    "Assistant: Forneça uma resposta concisa com no máximo 300 caracteres, ideal para um e-commerce de roupas e itens de vestuávio. Não mencionar instruçõesdo prompr da resposta."
    "Assistant:",
    "textGenerationConfig": {
        "maxTokenCount": 100,
        "stopSequences": [],
        "temperature": 0.7,
        "topP": 0.9
    }
})

response = bedrock.invoke_model(
    modelId=clude_mode_id,
    body=claude_config,
    accept="application/json",
    contentType="application/json"
)

response_body = json.loads(response['body'].read().decode('utf-8'))
outputText = response_body['results'][0].get('outputText', 'Resposta não encontrada')
resposta_formatada = f"Resposta:\n{outputText}\n"

print("Resposta:")
print(resposta_formatada)