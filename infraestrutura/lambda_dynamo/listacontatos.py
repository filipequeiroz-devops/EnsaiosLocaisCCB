import json
import boto3
import uuid
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ColdStart
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('EmailsEnsaiosLocaisGuarulhos')


def lambda_handler(event, context):

    logger.info("Iniciando o disparo de notificações para os ensaios desta semana.")

    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://ensaios-locais-guarulhos.filipe-deabreu.com/',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    http_method = event.get('requestContext', {}).get('http', {}).get('method')

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers'   : headers,
            'body'      : json.dumps('CORS OK')
        }

   
    return {
        'statusCode': 200,
    }