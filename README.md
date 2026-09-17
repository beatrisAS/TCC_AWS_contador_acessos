# 🚀 Contador de Acessos Serverless

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Serverless](https://img.shields.io/badge/Serverless-FD5750?style=for-the-badge&logo=serverless&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AWS CDK](https://img.shields.io/badge/AWS_CDK-cc292b?style=for-the-badge&logo=aws-api-gateway&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

Este repositório contém o código-fonte e a infraestrutura como código (IaC) do projeto **Contador de Acessos Serverless**, desenvolvido como Trabalho de Conclusão de Curso (TCC) para o **Programa AWS re/Start | Escola da Nuvem**.

## 📖 Visão Geral do Projeto

Uma startup parceira precisa lançar uma campanha de marketing através de uma *landing page* ("Em Breve"). O tráfego esperado é totalmente imprevisível, podendo variar de algumas dezenas a milhões de acessos simultâneos caso a campanha viralize. 

Soluções tradicionais baseadas em servidores virtuais (EC2) trariam dois grandes riscos:
1. **Superdimensionamento:** Desperdício financeiro com servidores ociosos.
2. **Subdimensionamento:** Queda da aplicação no momento crucial por falta de recursos.

A solução desenvolvida é uma arquitetura **100% Serverless**, garantindo alta disponibilidade nativa, escalabilidade elástica instantânea e um modelo financeiro altamente otimizado (*Pay-per-use*).

---

## 🏗️ Arquitetura da Solução

<!-- 📸 SUBSTITUA O CAMINHO ABAIXO PELA IMAGEM DO SEU DIAGRAMA DE ARQUITETURA -->
<div align="center">
  <img src="https://github.com/beatrisAS/TCC_AWS_contador_acessos/blob/main/Docs/Diagrama%20de%20Arquitetura.jpg" alt="Diagrama de Arquitetura" width="100%">
  <br>
  <em>Figura 1: Diagrama da arquitetura Serverless provisionada na AWS.</em>
</div>
<br>

O sistema é orientado a eventos e divide-se em três camadas principais, provisionadas de forma automatizada via **AWS CDK**:

### 1. Camada de Borda e Segurança (Edge Layer)
*   **Amazon S3:** Hospedagem do front-end estático (HTML/CSS/JS) de forma altamente durável.
*   **Amazon CloudFront:** CDN global que realiza o cache agressivo dos arquivos estáticos, reduzindo latência e chamadas diretas à origem.
*   **Origin Access Control (OAC):** Garante que o S3 só possa ser acessado através do CloudFront.
*   **AWS WAF:** Protege a aplicação contra bots, fraudes no contador e ataques DDoS.

### 2. Camada de Processamento (Compute Layer)
*   **Amazon API Gateway:** Exposição de endpoints RESTful seguros, recebendo as requisições assíncronas do front-end.
*   **AWS Lambda:** O "cérebro" da aplicação. Executa a lógica de negócios stateless (incremento do contador) em questão de milissegundos.

### 3. Camada de Persistência (Data Layer)
*   **Amazon DynamoDB:** Banco de dados NoSQL de altíssima performance operando em modo *On-Demand*. Garante a atomicidade com operações `UpdateItem`.
*   **DynamoDB TTL:** Política automatizada que deleta registros antigos após o término da campanha, otimizando custos a longo prazo.

---

## 🛡️ Segurança e Governança

*   **Princípio do Menor Privilégio:** Implementado via **AWS IAM**. O AWS Lambda possui uma *Role* estrita que permite apenas as ações `PutItem` e `UpdateItem` na tabela específica do DynamoDB.
*   **Auditoria Contínua:** Utilização do **AWS Trusted Advisor** para garantir conformidade com o *Well-Architected Framework*.
*   **FinOps:** Monitoramento via **Amazon CloudWatch**, controle estrito de teto de gastos utilizando **AWS Budgets** e alertas críticos via **Amazon SNS**.

---

## 💰 Viabilidade Financeira (Estimativa de Custos)

<!-- 📸 SUBSTITUA O CAMINHO ABAIXO PELA IMAGEM DA SUA ESTIMATIVA DE CUSTOS -->
<div align="center">
  <img src="https://github.com/beatrisAS/TCC_AWS_contador_acessos/blob/main/Docs/Estimativa%20de%20Custos.png" alt="Estimativa de Custos na AWS" width="80%">
  <br>
  <em>Figura 2: Estimativa de custos gerada pela AWS Pricing Calculator.</em>
</div>
<br>

Simulação realizada na calculadora oficial da AWS para **1 milhão de acessos mensais** (Região: `us-east-2` - Ohio):

*   **Custo de Implantação (Setup):** US$ 0,00
*   **Custo Mensal Estimado:** US$ 52,57
*   **Custo Anual Projetado:** US$ 630,84

Grande parte da economia provém da maximização do *AWS Free Tier* (Always Free) no Lambda e DynamoDB, além da delegação do bloqueio de ataques para a borda com o WAF, poupando processamento de backend.

---

## ⚙️ Implantação e Uso (CI/CD)

### Pré-requisitos
*   [Node.js](https://nodejs.org/) (Para o AWS CDK)
*   [Python 3.x](https://www.python.org/)
*   [AWS CLI](https://aws.amazon.com/cli/) configurado com suas credenciais.
*   [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) instalado globalmente (`npm install -g aws-cdk`).

### Passos para Deploy Local

1. Clone este repositório:
   ```bash
   git clone https://github.com/SEU-USUARIO/contador-acessos-serverless.git
   cd contador-acessos-serverless
   ```

2. Crie e ative o ambiente virtual Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts ctivate
   ```

3. Instale as dependências da infraestrutura:
   ```bash
   pip install -r requirements.txt
   ```

4. Realize o bootstrap da conta AWS e faça o deploy:
   ```bash
   cdk bootstrap
   cdk synth
   cdk deploy
   ```

### CI/CD com GitHub Actions
Este projeto utiliza GitHub Actions para integração e entrega contínuas. Qualquer push para a branch `main` executa testes, gera o CloudFormation Template e aplica as mudanças na infraestrutura AWS automaticamente.

---

## 👥 Equipe Desenvolvedora

*   Beatris Antunes Silva
*   Deivid Marcio Dos Santos Ferreira
*   Guilherme José Rodrigues Filho
*   Rafael De Matos Correa Figueiredo
*   William Dos Santos Martins

**Orientador:** Prof. Rubens Almeida de Andrade
