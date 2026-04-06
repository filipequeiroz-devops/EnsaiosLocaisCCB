#Processo de migração
#Antigamento o projeto aceita apenas emails, a ideia agora é aceitar emaile numero de telefone

import boto3

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')

def migrar_dados_antigos():
    response = table.scan()
    itens = response.get('Items', [])
    
    print(f"Iniciando verificação de {len(itens)} itens...")
    
    atualizados = 0
    for item in itens:
        if 'Emails' in item and 'Contato' not in item:
            email_valor = item['Emails']
            item_id = item['id']
            
            print(f"Atualizando registro {item_id} ({email_valor})...")
        
            table.update_item(
                Key={'id': item_id},
                UpdateExpression="SET Contato = :c, Tipo = :t",
                ExpressionAttributeValues={
                    ':c': email_valor,
                    ':t': 'email'
                }
            )
            atualizados += 1

    print(f"Migração concluída! {atualizados} registros foram normalizados.")

def remover_coluna_antiga():
    response = table.scan()
    itens = response.get('Items', [])
    
    print(f"Analisando {len(itens)} itens para remoção do campo antigo...")
    
    removidos = 0
    for item in itens:
        if 'Emails' in item and 'Contato' in item:
            item_id = item['id']
            
            print(f"Limpando registro {item_id}...")
            
            table.update_item(
                Key={'id': item_id},
                UpdateExpression="REMOVE Emails"
            )
            removidos += 1
        else:
            if 'Emails' in item:
                print(f"AVISO: O item {item['id']} tem 'Emails' mas NÃO tem 'Contato'. Pulando para segurança.")

    print(f"--- Limpeza concluída! ---")
    print(f"Atributo 'Emails' removido de {removidos} registros.")

if __name__ == "__main__":
    #migrar_dados_antigos()
    remover_coluna_antiga()
    