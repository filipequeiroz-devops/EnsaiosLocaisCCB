variable "email_user" {
  description = "E-mail do remetente para envio das notificações"
  type        = string
}

variable "email_pass" {
  description = "Senha do e-mail do remetente para envio das notificações"
  type        = string
}

variable "datadog_api_key" {
  description = "API Key do Datadog"
  type        = string
  sensitive   = true
}

variable "datadog_app_key" {
  description = "APP Key do Datadog"
  type        = string
  sensitive   = true
}

variable "senha_dynamo" {
  description = "Senha para acesso ao DynamoDB"
  type        = string
  sensitive   = true
}