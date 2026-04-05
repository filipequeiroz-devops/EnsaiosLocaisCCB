resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "api-ensaios-locais"
  protocol_type = "HTTP"
  
  # Configuração de CORS para permitir envio de dados
  cors_configuration {
    allow_origins = ["*"] # Em produção, coloque o domínio do seu site aqui
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }
}


resource "aws_apigatewayv2_stage" "lambda_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = "$default"
  auto_deploy = true
}

#Integra a API com a sua Função Lambda
resource "aws_apigatewayv2_integration" "lambda_integration" {
  api_id           = aws_apigatewayv2_api.lambda_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.cadastro_email_lambda.invoke_arn
}

#Definindo Rota para gravar emails
resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "POST /cadastro"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}

#Definindo Rota para gravar numeros de telefone
resource "aws_apigatewayv2_route" "lambda_route" {
  api_id    = aws_apigatewayv2_api.lambda_api.id
  route_key = "POST /cadastro-telefone"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration.id}"
}


#Permissao para a API chamar a função lambda
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cadastro_email_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*"
}

output "api_url" {
  value = "${aws_apigatewayv2_api.lambda_api.api_endpoint}/cadastro"
}