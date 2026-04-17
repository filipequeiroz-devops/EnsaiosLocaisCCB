# Lambda identity
resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_exec_role_ensaios"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Permissão para escrever no DynamoDB
resource "aws_iam_role_policy" "dynamo_write_policy" {
  name = "lambda_dynamo_write_policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = [
        "dynamodb:PutItem",
        "dynamodb:UpdateItem"
      ]
      Effect   = "Allow"
      Resource = "${aws_dynamodb_table.EmailsEnsaiosLocaisGuarulhos.arn}"
    },
    {
      # Permite que a Lambda grave logs
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Effect   = "Allow"
      Resource = "arn:aws:logs:*:*:*"
    },
    {
      #permite executa table scan
      Action = [
        "dynamodb:Scan"
      ]
      Effect   = "Allow"
      Resource = "${aws_dynamodb_table.EmailsEnsaiosLocaisGuarulhos.arn}"
    }
    
    ]
  })
}