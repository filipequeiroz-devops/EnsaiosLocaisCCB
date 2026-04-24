import unittest
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from infraestrutura.lambda_index.index import monta_html_email, enviar_email, lambda_handler

# Carregar variáveis de ambiente
load_dotenv()

class TestIndex(unittest.TestCase):

    def test_monta_html_email(self):
        resultado = monta_html_email("email", "test@example.com")
        self.assertIn("<html>", resultado)  # Verifica que é HTML
        self.assertIn("E-mail", resultado)  # Verifica que o 'tipo' está correto
        self.assertIn("test@example.com", resultado)  # Verifica que o contato está incluso


    @patch("infraestrutura.lambda_index.index.smtplib.SMTP_SSL")
    def test_enviar_email(self, mock_smtp):
      # Configura o mock para a classe SMTP_SSL
      mock_instance = MagicMock()
      mock_smtp.return_value.__enter__.return_value = mock_instance

      # Chama a função de envio de email
      enviar_email("dest@example.com", "<html>Test</html>")

      # Verifica fluxo de envio do e-mail
      mock_smtp.assert_called_once_with('smtp.gmail.com', 465)  # Verifica se a conexão foi criada
      mock_instance.login.assert_called_once_with(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))  # Valida login
      mock_instance.sendmail.assert_called_once()  # Verifica envio de email


    @patch("infraestrutura.lambda_index.index.table")
    @patch("infraestrutura.lambda_index.index.enviar_email")
    def test_lambda_handler_email(self, mock_email, mock_table):
        # Mockando a tabela DynamoDB
        mock_table.put_item = MagicMock()

        # Evento simulado do API Gateway
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": '{"tipo": "email", "contato": "test@example.com"}'
        }

        # Chamar o lambda
        response = lambda_handler(event, None)

        # Validar a resposta
        self.assertEqual(response["statusCode"], 200)
        self.assertIn("Cadastro realizado com sucesso!", response["body"])

        # Validar chamadas
        mock_table.put_item.assert_called()  # Verifica se o DynamoDB foi chamado
        mock_email.assert_called_with("test@example.com", mock_email.call_args[0][1]) # Verifica se o email foi enviado com o contato correto

    def test_lambda_handler_invalid_email(self):
        event = {
            "requestContext": {"http": {"method": "POST"}},
            "body": '{"tipo": "email", "contato": "invalid"}'
        }
        response = lambda_handler(event, None)
        self.assertEqual(response["statusCode"], 400)

if __name__ == "__main__":
    unittest.main()