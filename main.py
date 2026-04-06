import os
import pandas as pd
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

REGION     = "us-east-1" 
TABLE_NAME = "EmailsEnsaiosLocaisGuarulhos"

def buscar_emails_dynamo():
    """Busca apenas os contatos do tipo 'email' na tabela do DynamoDB."""
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table    = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    
    lista_emails = []
    # Percorre todos os itens retornados do banco
    for item in response.get('Items', []):
        # Filtra apenas se o 'Tipo' for 'email' e se o campo 'Contato' existir
        if item.get('Tipo') == 'email' and item.get('Contato'):
            lista_emails.append(item['Contato'])
            
    return lista_emails

def enviar_email(destinatarios, mensagem_html):
    remetente = os.environ.get('EMAIL_USER')
    senha = os.environ.get('EMAIL_PASS')
    
    if not remetente or not senha:
        print("Erro: Credenciais de e-mail não configuradas.")
        return

    # MIMEMultipart para o Gmail entender que é um e-mail rico
    msg = MIMEMultipart()
    msg['Subject'] = f"🔔 Aviso de Ensaio - {datetime.now().strftime('%d/%m/%Y')}"
    msg['From'] = f"Ensaios Guarulhos <{remetente}>"
    
    # Boa prática de segurança: Colocamos o seu próprio e-mail no "To" (Para).
    # Os destinatários reais vão direto no .sendmail(), funcionando como BCC (Cópia Oculta).
    msg['To'] = remetente

    # Anexando ao corpo do email
    msg.attach(MIMEText(mensagem_html, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remetente, senha)
            # Ao passar a lista 'destinatarios' aqui, e não no cabeçalho do e-mail, eles vão como cópia oculta
            server.sendmail(remetente, destinatarios, msg.as_string())
        print(f"E-mail enviado com sucesso para {len(destinatarios)} pessoas (em cópia oculta)!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def job():
    hoje       = datetime.now().strftime('%Y-%m-%d')
    df         = pd.read_csv('EnsaiosGuarulhos.csv') 
    df['data'] = df['data'].astype(str).str.strip()
    
    # Filtra TODOS os eventos de hoje
    eventos_hoje = df[df['data'] == hoje]

    if not eventos_hoje.empty:
        # inicio do html para a lista de eventos
        lista_eventos_html = ""
        
        # Percorre cada linha de evento encontrada para hoje
        for index, row in eventos_hoje.iterrows():
            local = row['Localidade']
            hora = row['Horário']
            waze = row['Waze']
            
            # Adiciona um bloco para cada ensaio na lista
            lista_eventos_html += f"""
            <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #007bff; margin-bottom: 20px; border-right: 1px solid #eee; border-top: 1px solid #eee; border-bottom: 1px solid #eee;">
                <p style="margin: 5px 0;">📍 <b>Local:</b> {local}</p>
                <p style="margin: 5px 0;">⏰ <b>Horário:</b> {hora}</p>
                <p style="margin: 10px 0 0 0;">
                    <a href="{waze}" style="color: #007bff; text-decoration: none; font-weight: bold;">🚗 Abrir no Waze</a>
                </p>
            </div>
            """

        # Monta o corpo final com a lista de eventos dentro
        corpo_html = f"""
        <html>
          <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #fff; padding: 30px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
              <h2 style="color: #007bff; text-align: center;">📢 Ensaios de Hoje em Guarulhos</h2>
              <p style="text-align: center; color: #666;">Identificamos os seguintes eventos para hoje, dia {datetime.now().strftime('%d/%m/%Y')}:</p>
              
              {lista_eventos_html}
              
              <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
              <p style="font-size: 12px; color: #999; text-align: center;">
                Este é um aviso automático do sistema Ensaios Guarulhos, desenvolvido por Filipe Queiroz de Abreu, do parque santos dumont.<br>
                Deus abençoe!
              </p>
            </div>
          </body>
        </html>
        """
        
        lista_emails = buscar_emails_dynamo()
        
        if lista_emails:
            enviar_email(lista_emails, corpo_html)
        else:
            print("Nenhum e-mail cadastrado no banco (ou nenhum do tipo 'email').")
    else:
        print(f"Nenhum evento agendado para hoje ({hoje}).")

if __name__ == "__main__":
    job()