# Compacta o código python em um .zip (exigência da AWS)
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda"
  output_path = "${path.module}/lambda_function_payload.zip"
}

resource "aws_lambda_function" "cadastro_email_lambda" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "CadastroEmailEnsaios"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "index.lambda_handler" # Nome do arquivo.nome da função
  runtime       = "python3.9"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.EmailsEnsaiosLocaisGuarulhos.name
      EMAIL_USER = var.email_user
      EMAIL_PASS = var.email_pass
    }
  }
}