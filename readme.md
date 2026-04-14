# 🎼 Automação - Notificação de Ensaios Locais em Guarulhos da Congregação Cristã no Brasil

**Language / Idioma**: [🇺🇸 English](#-project-overview) | [🇧🇷 Português](#-visão-geral-do-projeto)

<div align="center">

![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Amazon DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Amazon CloudFront](https://img.shields.io/badge/Amazon%20CloudFront-FF9900?style=for-the-badge&logo=amazoncloudfront&logoColor=white)
![Datadog](https://img.shields.io/badge/Datadog-632CA6?style=for-the-badge&logo=datadog&logoColor=white) 

</div>

---

## 🇺🇸 Project Overview

This project is a **Serverless Infrastructure** and **CI/CD** implementation. It automates the management and notification of local musical rehearsal schedules in Guarulhos, Brazil. The solution combines data processing, NoSQL storage, and a global content delivery network (CDN).

### 🏗️ Architecture & Workflow

1.  **Storage & Hosting:** A static website is hosted on **Amazon S3** and distributed globally via **Amazon CloudFront**.
2.  **Database:** **Amazon DynamoDB** stores subscriber emails and visitor demographic logs.
3.  **CI/CD Pipeline:** A dual-trigger **GitHub Actions** workflow:
    * **On Push:** Automatically syncs the `./App` directory to S3 and triggers a **CloudFront Invalidation** to clear the cache.
    * **On Schedule:** Runs daily to process rehearsal data and send email notifications.
4.  **Client-side:** **JavaScript** handles visitor tracking and interaction with the Serverless backend.

---

## 🇧🇷 Visão Geral do Projeto

Este projeto é uma implementação de **Infraestrutura Serverless** e **CI/CD**. Ele automatiza o gerenciamento e a notificação de cronogramas de ensaios musicais em Guarulhos da Congregação Cristã no Brasil. A solução combina processamento de dados, armazenamento NoSQL e uma rede de entrega de conteúdo global (CDN).

### 🏗️ Arquitetura e Fluxo

1.  **Hospedagem:** O site estático é hospedado no **Amazon S3** e distribuído globalmente via **Amazon CloudFront**.
2.  **Banco de Dados:** O **Amazon DynamoDB** armazena e-mails de inscritos.
3.  **Pipeline CI/CD:** Um workflow do **GitHub Actions** com dois gatilhos:
    * **No Push:** Sincroniza automaticamente a pasta `./App` com o S3 e dispara uma **Invalidação de Cache** no CloudFront.
    * **No Schedule:** Roda diariamente para processar dados de ensaios e enviar notificações por e-mail.
4.  **Client-side:** **JavaScript** gerencia o rastreamento de visitantes e a interação com o backend Serverless.

### 🚀 Como Rodar Localmente

1.  Clone este repositório.
2.  Instale as dependências:
    ```bash
    pip install pandas boto3
    ```
3.  Configure suas credenciais AWS e segredos do GitHub para habilitar a automação completa.

---

<div align="center">
  <sub>Developed by **Filipe Queiroz** as part of a DevOps & Cloud Infrastructure Portfolio.</sub>
</div>