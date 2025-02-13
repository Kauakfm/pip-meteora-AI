import boto3
import json
import sqlite3
from langchain_aws import BedrockLLM
from langchain_core.prompts import ChatPromptTemplate


conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()
bedrock_client = boto3.client(service_name = 'bedrock-runtime', region_name='us-east-1')

def configurar_modelo(client, max_tokens=200, temperature=0.5):
    return BedrockLLM(
    model_id='amazon.titan-text-express-v1', 
    client=client,
    max_tokens=max_tokens,   
    temperature=temperature,          
    )

modelo = configurar_modelo(bedrock_client)

historico = []

def get_hist():
    return "\n".join(historico)


def consulta_produto(nome_produto):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM roupas WHERE nome LIKE ?", ('%' + nome_produto + '%',))
    resultado = cursor.fetchall()
    
    conn.close()
    return resultado


def get_chat_prompt(entrada):
    template = ChatPromptTemplate.from_messages(
        [
            ("system", 
            "Você é um assistente virtual especializado em moda para e-commerce. "
            "Sua função é fornecer respostas concisas e úteis sobre produtos de vestuário. "
            "Responda apenas a perguntas relacionadas a roupas e acessórios de moda. "
            "Se a pergunta não for sobre moda, redirecione o usuário para questões relacionadas. "
            "Se baseie nos dados disponíveis para fornecer respostas precisas."),
            
            ("human", entrada),
            
            ("assistant", 
            "Você é um assistente virtual especializado em moda para e-commerce. "
            "Sua função é fornecer respostas concisas e úteis sobre produtos de vestuário. "
            "Responda apenas a perguntas relacionadas a roupas e acessórios de moda. "
            "Se a pergunta não for sobre moda, redirecione o usuário para questões relacionadas. "
            "Se baseie nos dados disponíveis para fornecer respostas precisas."
            "Forneça uma resposta concisa, direta e útil com no máximo 300 caracteres. "
            "Não mencione o fato de estar baseando sua resposta em um prompt. "
            "Se não houver dados disponíveis no banco de dados, oriente o usuário a tentar outra busca ou fornecer mais detalhes.")
        ]
    )
    return template

def inv_modelo(prompt):
    produtos_encontrados = consulta_produto(prompt)
    if produtos_encontrados:
        produtos_info = "\n".join([f"{p[0]}: {p[1]}, Preço: {p[2]}, Quantidade: {p[3]}" for p in produtos_encontrados])
        prompt = f"Produtos disponíveis: {produtos_info}\n{prompt}"
    else:
        prompt = f"Nenhum produto encontrado para '{prompt}'.\n{prompt}"
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
