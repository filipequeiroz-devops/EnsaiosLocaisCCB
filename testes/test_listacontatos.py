import unittest
import boto3
import os
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv

load_dotenv()

from infraestrutura.lambda_dynamo.listacontatos import buscar_emails_dynamo, buscar_telefones_dynamo, lambda_handler

dynamodb     = boto3.resource('dynamodb')
table        = dynamodb.Table(os.getenv('TABLE_NAME'))
senha_dynamo = os.getenv('SENHA_DYNAMO')

class TestMain(unittest.TestCase):
    
    def test_buscar_telefones_dynamo_valid(self): 
        # Mock da tabela DynamoDB
        mock_table = MagicMock()
        mock_table.scan.return_value = {
            'Items': [
                {'Tipo': 'telefone', 'Contato': '123456789'},
                {'Tipo': 'email', 'Contato': 'joao@example.com'},
                {'Tipo': 'telefone', 'Contato': '987654321'}
            ]
        }
    
        result = buscar_telefones_dynamo(mock_table)
        self.assertEqual(result, ['123456789', '987654321']) 
    
    def test_buscar_telefones_dynamo_no_items(self): 
        
        # Mock da tabela DynamoDB
        mock_table = MagicMock()
        mock_table.scan.return_value = {'Items': []}
    
        result = buscar_telefones_dynamo(mock_table)
        self.assertEqual(result, [])
    
    def test_buscar_telefones_dynamo_invalid_items(self): 
        
        # Mock da tabela DynamoDB
        mock_table = MagicMock()
        mock_table.scan.return_value = {
            'Items': [
                {'Tipo': 'email', 'Contato': 'joao@example.com'},
                {'Contato': '123456789'},
                {'Tipo': 'telefone'}
            ]
        }
    
        result = buscar_telefones_dynamo(mock_table)
        self.assertEqual(result, [])
    
    def test_lambda_handler_authorization(self): 
        
        mock_event = {
            'httpMethod': 'GET',
            'headers': {'Authorization': 'Bearer TEST_KEY'}
        }
    
        with patch('infraestrutura.lambda_dynamo.listacontatos.senha_dynamo', 'TEST_KEY'), \
             patch('infraestrutura.lambda_dynamo.listacontatos.buscar_emails_dynamo', return_value=[]), \
             patch('infraestrutura.lambda_dynamo.listacontatos.buscar_telefones_dynamo', return_value=[]):
    
            result = lambda_handler(mock_event, None)
            self.assertEqual(result['statusCode'], 200)
            self.assertTrue('emails' in result['body'] and 'telefones' in result['body'])
    
    def test_lambda_handler_unauthorized(self): 
        
        mock_event = {
            'httpMethod': 'GET',
            'headers': {'Authorization': 'Invalid_Key'}
        }
    
        with patch('infraestrutura.lambda_dynamo.listacontatos.senha_dynamo', 'TEST_KEY'):
            result = lambda_handler(mock_event, None)
            self.assertEqual(result['statusCode'], 401)
    
    def test_lambda_handler_http_methods(self): 
        
        mock_event = {'httpMethod': 'POST'}
        result = lambda_handler(mock_event, None)
        self.assertEqual(result['statusCode'], 405)
    
    def test_buscar_emails_dynamo_valid(self):
        # Mock da tabela DynamoDB
        mock_table = MagicMock()
        mock_table.scan.return_value = {
            'Items': [
                {'Tipo': 'email', 'Contato': 'joao@example.com'},
                {'Tipo': 'telefone', 'Contato': '123456789'},
                {'Tipo': 'email', 'Contato': 'maria@example.com'}
            ]
        }
    
        result = buscar_emails_dynamo(mock_table)
        self.assertEqual(result, ['joao@example.com', 'maria@example.com'])
    
    def test_buscar_emails_dynamo_no_items(self): 
        # Mock da tabela DynamoDB
        mock_table = MagicMock()
        mock_table.scan.return_value = {'Items': []}
    
        result = buscar_emails_dynamo(mock_table)
        self.assertEqual(result, [])
    
    def test_buscar_emails_dynamo_invalid_items(self):
        # Mock da tabela DynamoDB
        mock_table = MagicMock()
        mock_table.scan.return_value = {
            'Items': [
                {'Tipo': 'telefone', 'Contato': '123456789'},
                {'Contato': 'joao@example.com'},
                {'Tipo': 'email'}
            ]
        }
    
        result = buscar_emails_dynamo(mock_table)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()