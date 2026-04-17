resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "api-ensaios-locais"
  protocol_type = "HTTP"

 
  
  # Configuração de CORS para permitir envio de dados
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }
}


resource "aws_apigatewayv2_stage" "lambda_stage" {
  api_id      = aws_apigatewayv2_api.lambda_api.id
  name        = "$default"
  auto_deploy = true

   # Proteção manual contra possíveis ataques DDoS, limitando o número de requisições
  default_route_settings {
  throttling_burst_limit = 3 # Máximo de requisições simultâneas em um pico
  throttling_rate_limit  = 1   # Número constante de requisições por segundo (RPS)
  }

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
##########################################################
#criando uma segunda API apenas listar os cadastro
##########################################################

resource "aws_apigatewayv2_api" "lambda_api_2" {
  name          = "api-ensaios-locais-listar"
  protocol_type = "HTTP"

 
  
  cors_configuration {
    allow_origins = ["*"] 
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }
}


resource "aws_apigatewayv2_stage" "lambda_stage2" {
  api_id      = aws_apigatewayv2_api.lambda_api_2.id
  name        = "$default"
  auto_deploy = true

  default_route_settings {
  throttling_burst_limit = 3 # Máximo de requisições simultâneas em um pico
  throttling_rate_limit  = 1   # Número constante de requisições por segundo (RPS)
  }
}

resource "aws_apigatewayv2_integration" "lambda_integration2" {
  api_id           = aws_apigatewayv2_api.lambda_api_2.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.Lista_Contatos_Lambda.invoke_arn
}


resource "aws_apigatewayv2_route" "lambda_route2" {
  api_id    = aws_apigatewayv2_api.lambda_api_2.id
  route_key = "GET /listar"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_integration2.id}"
}


resource "aws_lambda_permission" "api_gw2" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.Lista_Contatos_Lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.lambda_api_2.execution_arn}/*/*"
}

output "api_url2" {
  value = "${aws_apigatewayv2_api.lambda_api_2.api_endpoint}/listar"
}
  