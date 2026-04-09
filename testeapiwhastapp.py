
# vaqui eu quis testar como as mensagens ficariam no whatsapp, usando o mesmo formato de separadores simples que usei no email, para ver se fica legível ou se preciso usar outro format
# Precisei usar separadores simples (;) porque o WhatsApp não aceita mais do que 4 quebras de linha na mensagem do template, e queria manter uma estrutura clara para o usuário mesmo sem as quebras. O resultado ficou legível
# Ficou legível... mas não era o que eu queria... .


import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import urllib.request
import json
load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

#Crando uma data Teste
data_str = "2026-04-10 17:58:11.975078"
data = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S.%f")

hoje       = data.strftime('%Y-%m-%d')
df         = pd.read_csv('EnsaiosGuarulhos.csv') 
df['data'] = df['data'].astype(str).str.strip()
    
# Filtra TODOS os eventos de hoje
eventos_hoje = df[df['data'] == hoje]
    
# Percorre cada linha de evento encontrada para hoje


def enviar_mensagem_whatsapp(telefone_destino, data, ensaios):
    
    url = f"https://graph.facebook.com/v25.0/{os.environ.get('whatsapp_business_phone_number_id')}/messages"

    headers = {
        'Authorization'  : f'Bearer {os.environ.get("access_token")}',
        'Content-Type'   : 'application/json',
        'accept'         : '*/*'
    }

    payload = {
    "messaging_product": "whatsapp",
    "to": telefone_destino,
    "type": "template",
    "template": {
        "name": "aviso_ensaios",
        "language": {
            "code": "pt_BR"
        },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": data
                    },
                    {
                        "type": "text",
                        "text": ensaios
                    }
                ]
            }
        ]
    }
    }

    data_bytes = json.dumps(payload).encode('utf-8')
    req        = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            print(f"Sucesso! Status: {response.getcode()}")
    except urllib.error.HTTPError as e:
        # Lendo o corpo do erro 400
        corpo_erro = e.read().decode('utf-8')
        print(f"Erro detalhado da Meta: {corpo_erro}")
    except Exception as e:
        print(f"Erro genérico: {str(e)}")


ensaios = ""
for index, row in eventos_hoje.iterrows():
    local = row['Localidade']
    hora = row['Horário']
    # Usando separadores simples em vez de quebras de linha
    ensaios += f"📍 Local: {local} | ⏰ Hora: {hora}; "

# Remove o último ponto e vírgula se quiser
ensaios = ensaios.strip("; ")


print(os.environ.get('whatsapp_business_phone_number_id'))
print(os.environ.get('access_token'))
print(len(ensaios))
enviar_mensagem_whatsapp("5511968597371", "04/04/2026",ensaios)