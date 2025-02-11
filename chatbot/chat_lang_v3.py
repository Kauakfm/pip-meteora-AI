import boto3
import json
from langchain_aws import BedrockLLM
from langchain_core.prompts import ChatPromptTemplate

bedrock_client = boto3.client(service_name = 'bedrock-runtime', region_name='us-east-1')

modelo = BedrockLLM(model_id='amazon.titan-text-express-v1', client=bedrock_client)

historico = []

def get_hist():
    return "\n".join(historico)

def get_chat_prompt(entrada):
    template = ChatPromptTemplate.from_messages(
        [
            ("system", "Você é um assistente virtual especializado em moda para e-commerce. Forneça respostas concisas e úteis."),
            ("human", entrada),
            ("assistant", "Forneça uma resposta concisa com no máximo 200 caracteres, ideal para um e-commerce de roupas e itens de vestuário. Não mencionar instruções do prompt na resposta.")
        ]
    )
    return template

def inv_modelo(prompt):
    chain = get_chat_prompt(prompt).pipe(modelo)
    response = chain.invoke({"product_name": prompt})
    return response

print(
    f"Assitente: Olá Sou eu Assistente Virtual. :) \n"
    "Em que posso ajudar hoje?"
)

while True:
    entrada = input("User: ")
    historico.append(f"Human: {entrada}")
    if entrada.lower() == "sair":
        break
    resposta = inv_modelo(entrada)
    resposta_formatada = f"Assistence:\n{resposta}\n"
    historico.append(f"Assistant: {resposta_formatada}")
    print(resposta_formatada)

