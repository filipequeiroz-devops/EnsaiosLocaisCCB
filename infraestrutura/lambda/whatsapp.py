import json
import os
import boto3

lambda_client = boto3.client('lambda')

PRIVATE_LAMBDA_NAME = os.environ.get('PRIVATE_LAMBDA_NAME')
MAX_CHARS = 800

# ==========================================
# This is the meta's painel password
# ==========================================
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

def lambda_handler(event, context):
    try:
        # ==========================================
        # CORREÇÃO: Busca o método HTTP de forma segura para API v1 e v2
        # ==========================================
        http_method = event.get('httpMethod') 
        if not http_method:
            http_method = event.get('requestContext', {}).get('http', {}).get('method')
            
        if not http_method:
            print("Formato de evento desconhecido:", json.dumps(event))
            return {'statusCode': 400, 'body': 'Metodo HTTP nao encontrado'}

        # ==========================================
        # WebHook Validation by GET request from Meta
        # ==========================================
        if http_method == 'GET':
            # Usa 'or {}' porque se não houver params, a AWS manda None e quebra o código
            query_params = event.get('queryStringParameters') or {}   
            mode         = query_params.get('hub.mode')
            token        = query_params.get('hub.verify_token')
            challenge    = query_params.get('hub.challenge')
            
            # If meta's token matches our token, we confirm the webhook setup by returning the challenge
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("Webhook verificado com sucesso pela Meta!")
                return {
                    'statusCode': 200,
                    'body': challenge
                }
            else:
                print(f"Falha de token. Esperado: {VERIFY_TOKEN}, Recebido: {token}")
                return {'statusCode': 403, 'body': 'Falha na verificação do Token'}

        # ==========================================
        # 2. RECEBENDO MENSAGENS (O POST do cliente)
        # ==========================================
        elif http_method == 'POST':
            body_str = event.get('body', '{}')
            parsed_body = json.loads(body_str)
            
            try:
                entry = parsed_body['entry'][0]
                changes = entry['changes'][0]
                value = changes['value']
                
                if 'messages' not in value:
                    return {'statusCode': 200, 'body': 'Evento ignorado'}
                    
                message_data = value['messages'][0]
                telefone_cliente = message_data['from']
                
                if message_data['type'] == 'text':
                    mensagem_do_cliente = message_data['text']['body']
                else:
                    return {'statusCode': 200, 'body': 'Tipo de mensagem não suportado'}
                    
            except KeyError:
                return {'statusCode': 200, 'body': 'Payload não reconhecido'}

            if len(mensagem_do_cliente) > MAX_CHARS:
                print(f"ALERTA SECURITY: Mensagem longa bloqueada. {len(mensagem_do_cliente)} chars")
                return {'statusCode': 200, 'body': 'Mensagem bloqueada por tamanho'}
            
            payload_limpo = {
                'telefone': telefone_cliente,
                'mensagem': mensagem_do_cliente
            }
            
            print("Enviando para a Lambda Privada processar com o Bedrock...")
            lambda_client.invoke(
                FunctionName=PRIVATE_LAMBDA_NAME,
                InvocationType='Event', 
                Payload=json.dumps(payload_limpo)
            )
            
            return {'statusCode': 200, 'body': 'EVENT_RECEIVED'}
            
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        return {'statusCode': 500, 'body': 'Erro interno'}