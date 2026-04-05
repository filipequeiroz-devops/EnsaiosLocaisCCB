import json
import os
import boto3
import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ColdStart
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')

def monta_html_email(email_usuario):
    html = f"""
    <html>
    <body>
        <h2>🚨 Novo Cadastro de E-mail 🚨</h2>
        <p>Olá,</p>
        <p>O e-mail <strong>{email_usuario}</strong> foi cadastrado com sucesso para receber notificações dos ensaios locais em Guarulhos.</p>
        <p>Obrigado por se inscrever!</p>
        <br>
    </body>
    </html>
    """
    return html

def enviar_email(destinatario, mensagem_html):
    remetente    = os.environ.get('EMAIL_USER')
    senha        = os.environ.get('EMAIL_PASS')
    destinatario = os.environ.get('EMAIL_USER') #um email paea  mim mesmo, para testar o envio de email, depois pode ser modificado para enviar para os emails cadastrados no DynamoDB

     # MIMEMultipart para o Gmail entender que é um e-mail rico, ou seja, poder usar sintaxe HTML e deixar o e-mail mais bonito
    msg = MIMEMultipart()
    msg['Subject'] = f"🚨 Aviso De Cadastro- {datetime.now().strftime('%d/%m/%Y')}"
    msg['From']    = f"Ensaios Guarulhos <{remetente}>"
    msg['To']      = destinatario
    msg.attach(MIMEText(mensagem_html, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            # enviando o msg.as_string() que contém o HTML formatado
            server.sendmail(remetente, destinatario, msg.as_string())
        
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


def lambda_handler(event, context):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
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

    # Pegando o corpo da requisição e convertendo de string para JSON
    try:
        body_str = event.get('body', '{}')
        body = json.loads(body_str)
        email_usuario = body.get('email')

        if not email_usuario:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps('Email nao fornecido no JSON')
            }

        # Grava no dynamoDB, gerando um ID único para cada email
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'Emails': email_usuario
            }
        )

        # Envia aviso de cadastro
        html_email = monta_html_email(email_usuario)
        enviar_email(email_usuario, html_email)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('E-mail cadastrado com sucesso!')
        }

    except Exception as e:
        # Se der erro no banco, retorna o erro com os Headers de CORS
        # para que o navegador exiba o erro real em vez de travar no CORS
        print(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps(f'Erro interno: {str(e)}')
        }