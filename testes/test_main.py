import unittest
from unittest.mock import patch, MagicMock
from main import job, enviar_email
import os
from dotenv import load_dotenv 

load_dotenv()

class TestMain(unittest.TestCase):
    
    @patch("main.smtplib.SMTP_SSL")
    def test_enviar_email(self, mock_smtp):
      # Configura o mock para a classe SMTP_SSL
      mock_instance = MagicMock()
      mock_smtp.return_value.__enter__.return_value = mock_instance

      # Chama a função de envio de email
      enviar_email("dest@example.com", "<html>Test</html>")

      # Verifica fluxo de envio do e-mail
      mock_smtp.assert_called_once_with('smtp.gmail.com', 465)  # Verifica se a conexão foi criada
      mock_instance.login.assert_called_once_with(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))  # Valida login


if __name__ == "__main__":
    unittest.main()