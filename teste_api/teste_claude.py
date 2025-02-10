import boto3
import json

bedrock = boto3.client(service_name = 'bedrock-runtime', region_name='us-east-1')
clude_mode_id = 'amazon.titan-text-express-v1'

claude_config = json.dumps({
    "inputText": "Human: Opções de sandália para uma caminhada na praia. Assistant;",
    "textGenerationConfig": {
        "maxTokenCount": 200,
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

response_body = response['body'].read().decode('utf-8')
print("Resposta:")
print(response_body)