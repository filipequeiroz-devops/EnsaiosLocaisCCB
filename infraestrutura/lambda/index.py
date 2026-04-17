import json
import os
import boto3
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ColdStart
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')

def monta_html_email(tipo_cadastro, contato_usuario):
    tipo_formatado = "E-mail" if tipo_cadastro == "email" else "WhatsApp (Telefone)"
    
    html = f"""
    <html>
    <body>
        <h2>🚨 Novo Cadastro de Contato 🚨</h2>
        <p>Olá,</p>
        <p>Um novo usuário acabou de se inscrever para os ensaios em Guarulhos.</p>
        <ul>
            <li><strong>Tipo:</strong> {tipo_formatado}</li>
            <li><strong>Contato:</strong> {contato_usuario}</li>
        </ul>
        <p>Obrigado por acompanhar o sistema!</p>
        <br>
    </body>
    </html>
    """
    return html

def enviar_email(destinatario, mensagem_html):
    remetente    = os.environ.get('EMAIL_USER')
    senha        = os.environ.get('EMAIL_PASS')
    destinatario = os.environ.get('EMAIL_USER')

    msg = MIMEMultipart()
    msg['Subject'] = f"🚨 Aviso De Cadastro - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From']    = f"Ensaios Guarulhos <{remetente}>"
    msg['To']      = destinatario
    msg.attach(MIMEText(mensagem_html, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
        
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")



def lambda_handler(event, context):

    logger.info("Iniciando o disparo de notificações para os ensaios desta semana.")

    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://ensaios-locais-guarulhos.filipe-deabreu.com/',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    http_method = event.get('requestContext', {}).get('http', {}).get('method')

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS OK')
        }

    try:
        body_str = event.get('body', '{}')
        body     = json.loads(body_str)
        
        # Pega os contatos do frontend
        tipo    = body.get('tipo')
        contato = body.get('contato')

        # Validação simples
        if not tipo or not contato:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('Dados incompletos: informe o tipo e o contato.')
            }

        # Grava no DynamoDB
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'Tipo': tipo, 
                'Contato': contato,
                'DataCadastro': datetime.now().isoformat()
            }
        )

        #  Alerta de cadastro: Envia para mim mesmo um e-mail toda vez que alguém se cadastrar (seja por WhatsApp ou E-mail)
        html_email = monta_html_email(tipo, contato)
        enviar_email(contato, html_email)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('Cadastro realizado com sucesso!')
        }

    except Exception as e:
        logger.error(f"Erro ao cadastrar contato: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Erro interno: {str(e)}')
        }