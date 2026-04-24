data "archive_file" "lambda_dynamo_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_dynamo"
  output_path = "${path.module}/lambda_function_payload_2.zip"
}

resource "aws_lambda_function" "Lista_Contatos_Lambda" {
  filename      = data.archive_file.lambda_dynamo_zip.output_path
  function_name = "Lista_ContatosEnsaios"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "datadog_lambda.handler.handler"
  runtime       = "python3.9"

  layers = [
    "arn:aws:lambda:us-east-1:464622532012:layer:Datadog-Extension:95",
    "arn:aws:lambda:us-east-1:464622532012:layer:Datadog-Python39:123"
  ]

  source_code_hash = data.archive_file.lambda_dynamo_zip.output_base64sha256

  environment {
    variables = {
      TABLE_NAME                     = aws_dynamodb_table.EmailsEnsaiosLocaisGuarulhos.name
      EMAIL_USER                     = var.email_user
      EMAIL_PASS                     = var.email_pass
      DD_LAMBDA_HANDLER              = "listacontatos.lambda_handler" # Especifica o handler para a extensão do Datadog (Nome do arquivo.nome da função)
      DD_API_KEY                     = var.datadog_api_key
      DD_SITE                        = "us5.datadoghq.com"
      DD_ENV                         = "producao"
      DD_SERVICE                     = "EnbsaiosLocaisLambda"
      DD_VERSION                     = "1.0.0"
      DD_TAGS                        = "tenant:EnsaiosLocais"
      DD_SERVERLESS_LOGS_ENABLED     = "true"
      SENHA_DYNAMO                   = var.senha_dynamo
    }
  }
}