import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')

def buscar_emails_dynamo():
    """Busca todos os e-mails cadastrados na tabela do DynamoDB."""
    response = table.scan()
    # Retorna uma lista apenas com os endereços de e-mail
    return [item['Emails'] for item in response.get('Items', [])]

emails = buscar_emails_dynamo()

boo = "sonic.sonic08@gmail.com" in emails
print(boo)