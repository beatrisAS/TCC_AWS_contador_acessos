# 🚀 AWS Serverless: Contador de Acessos

Projeto acadêmico conceitual desenvolvido durante o programa **AWS re/Start** pela Escola da Nuvem.

---
📋 **Sobre o projeto:**

Este repositório contém a arquitetura e a estrutura de código de uma solução Serverless para contagem de acessos em tempo real. O cenário simula o lançamento de uma campanha de marketing de um novo produto com uma página de "Em Breve". 

O principal desafio resolvido por esta arquitetura é a imprevisibilidade de tráfego, podendo variar de 10 a 1 milhão de acessos simultâneos, mantendo alta escalabilidade e baixo custo operacional através do modelo de cobrança sob demanda (*pay-as-you-go*).

---
💡 **Destaque Principal:**

Como se trata de um projeto acadêmico e conceitual (sem acesso para *deploy* real na AWS), toda a infraestrutura backend foi construída utilizando **Infraestrutura como Código (IaC) com AWS CDK em Python**. Para fins de demonstração e apresentação visual do fluxo, o frontend conta com um *Mock* inteligente integrado ao armazenamento local do navegador, simulando o comportamento real de um banco de dados na nuvem.

---
📌 **Funcionalidades:**

- Arquitetura 100% Serverless desenhada para alta disponibilidade
- Provisionamento automatizado de infraestrutura via AWS CDK
- Página web estática responsiva simulando o lançamento de uma campanha ("Em Breve")
- Simulação de incremento de acessos em tempo real integrando frontend e banco de dados simulado
- Gerenciamento de permissões seguro seguindo o Princípio do Menor Privilégio (IAM)
---
🛠️ **Tecnologias:**

| Camada | Tecnologia |
| :--- | :--- |
| **Infraestrutura como Código** | AWS CDK (Python) |
| **Computação em Nuvem (Backend)** | AWS Lambda (Python 3.9) |
| **Banco de Dados** | Amazon DynamoDB (NoSQL) |
| **Gerenciamento de API** | Amazon API Gateway |
| **Segurança e Permissões** | AWS IAM |
| **Front-end** | HTML5, CSS3, JavaScript (Vanilla) |
---
🌐 **Como executar:**
1. Abra o **Git Bash** e clone o repositório:
```bash
git clone https://github.com/beatrisAS/TCC_AWS_contador_acessos.git
```
2. Entre na pasta do projeto e abra o front-end:
```bash
cd contador-de-acessos-aws/frontend
```
3. Visualização no navegador:
 ```bash  
Dê um duplo clique no arquivo 'index.html' para abri-lo diretamente no seu navegador.
Pressione F5 ou atualize a página para simular o incremento de acessos (comportamento Lambda + DynamoDB).
```
---
👥 **Equipe:**

- Alexandra Prudencio Domiciano
- Beatris Antunes Silva
- Deivid Marcio Dos Santos Ferreira
- Guilherme José Rodrigues Filho
- Rafael De Matos Correa Figueiredo
- William Dos Santos Martins
---
📄 **Licença:**

Este projeto foi desenvolvido para fins acadêmicos e educacionais no âmbito do programa **AWS re/Start** · Escola da Nuvem · 2026.
