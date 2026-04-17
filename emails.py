import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')



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


emails    = buscar_emails_dynamo(table)
telefones = buscar_telefones_dynamo(table)
print("Contatos do tipo 'email':")
print(emails)
print("====================================")
print("Contatos do tipo 'telefone':")
print(telefones)
print("=================")
