import json
import boto3
import uuid
from datetime import datetime
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ColdStart
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table(os.getenv('TABLE_NAME'))
senha_dynamo = os.getenv('SENHA_DYNAMO')

def buscar_emails_dynamo(table):
    """Busca apenas os contatos do tipo 'email' na tabela do DynamoDB."""

    response = table.scan()
    
    lista_emails = []
    # Percorre todos os itens retornados do banco
    for item in response.get('Items', []):
        # Filtra apenas se o 'Tipo' for 'email' e se o campo 'Contato' existir
        if item.get('Tipo') == 'email' and item.get('Contato'):
            lista_emails.append(item['Contato'])
    return lista_emails

def buscar_telefones_dynamo(table):
    """Busca apenas os contatos do tipo 'telefone' na tabela do DynamoDB."""

    response = table.scan()
    
    lista_telefones = []
    # Percorre todos os itens retornados do banco
    for item in response.get('Items', []):
        # Filtra apenas se o 'Tipo' for 'telefone' e se o campo 'Contato' existir
        if item.get('Tipo') == 'telefone' and item.get('Contato'):
            lista_telefones.append(item['Contato'])
    return lista_telefones


def lambda_handler(event, context):
    logger.info("Iniciando listagem de contatos cadastrados no DynamoDB.")

    # 1. Removida a senha do Dynamo dos headers de RESPOSTA por segurança.
    # Adicionado 'Authorization' no Allow-Headers para o CORS funcionar com o seu token.
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*', 
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization' 
    }

    # 2. Captura o método de forma compatível com REST API (v1) e HTTP API (v2)
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers'   : headers,
            'body'      : json.dumps('CORS OK')
        }

    if http_method == 'GET':
        event_headers = event.get('headers', {})
        auth_header = event_headers.get('Authorization') or event_headers.get('authorization')
        
        if auth_header != f'Bearer {senha_dynamo}':
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps('Unauthorized')
            }
        
        else:
            try:
                lista_emails = buscar_emails_dynamo(table)
                lista_telefones = buscar_telefones_dynamo(table)

                response_body = {
                    'emails': lista_emails,
                    'telefones': lista_telefones
                }

                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps(response_body)
                }
            except Exception as e:
                logger.error(f"Erro ao buscar contatos no DynamoDB: {str(e)}")
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps('Erro interno ao buscar contatos')
                }
                
    return {
        'statusCode': 405, 
        'headers': headers,
        'body': json.dumps(f'Metodo HTTP não suportado: {http_method}')
    }