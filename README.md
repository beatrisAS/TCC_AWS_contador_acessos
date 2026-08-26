# 🚀 AWS Serverless: Contador de Acessos

Projeto acadêmico conceitual desenvolvido durante o programa **AWS re/Start** pela Escola da Nuvem.

---
📋 **Sobre o projeto:**

Este repositório contém a arquitetura e a estrutura de código de uma solução Serverless para contagem de acessos em tempo real. O cenário simula o lançamento de uma campanha de marketing de um novo produto com uma página de "Em Breve". 

O principal problema resolvido por esta arquitetura é a **imprevisibilidade de tráfego**. Como o volume pode variar de 10 a 1 milhão de acessos simultâneos, a solução foca em alta escalabilidade, resiliência e baixo custo operacional, evitando subdimensionamento (quedas do servidor) ou superdimensionamento (desperdício de dinheiro com recursos ociosos), através do modelo de cobrança sob demanda (*pay-as-you-go*).

---
🏗️ **Arquitetura e Decisões Técnicas:**

O projeto segue o modelo de 3 camadas da AWS e as melhores práticas do *Well-Architected Framework*:
- **Camada de Acesso (API Gateway):** A porta de entrada segura que recebe os cliques. Escolhido por ser nativamente Serverless e gerenciar picos de requisições de forma automática.
- **Camada de Processamento (AWS Lambda):** O "cérebro" event-driven. Escolhido no lugar do EC2 porque escala a zero e cobra apenas pelo tempo de execução em milissegundos.
- **Camada de Dados (DynamoDB):** Banco de dados super rápido. Escolhido no lugar do RDS pela performance extrema em acessos simples de chave-valor (utilizando a Partition Key fixa `"id": "hits"`).
- **Segurança (IAM):** Permissões restritas baseadas no Princípio do Menor Privilégio. O Lambda tem apenas permissão de `UpdateItem` na tabela específica, sem acesso total.
- **Gestão de Custos:** A arquitetura foca no AWS Free Tier. Em um cenário real com picos altos, a AWS Pricing Calculator demonstra que essa abordagem elimina os custos base de instâncias ociosas.

---
💡 **Destaque Principal (Pronto para o Mercado):**

Para demonstrar maturidade técnica e facilitar a replicação **sem gerar custos** para quem testar, implementamos uma **"Mini Nuvem" utilizando LocalStack e Docker**. 

Toda a infraestrutura backend foi construída utilizando **Infraestrutura como Código (IaC) com AWS CDK em Python**. Em vez de usar um simples *mock* simulado no front-end, o projeto levanta os serviços da AWS (Lambda, API Gateway e DynamoDB) localmente em contêineres Docker, simulando perfeitamente o ambiente real e corporativo da nuvem.

---
📌 **Funcionalidades:**

- Arquitetura 100% Serverless desenhada para alta disponibilidade.
- Provisionamento automatizado de infraestrutura via AWS CDK.
- Página web estática responsiva simulando o lançamento de uma campanha ("Em Breve").
- **Diferencial:** Ambiente isolado via Docker (LocalStack) reproduzindo a AWS localmente.
- Gerenciamento de permissões seguro seguindo o Princípio do Menor Privilégio (IAM).

---
🛠️ **Tecnologias:**

| Camada | Tecnologia |
| :--- | :--- |
| **Simulação Local Cloud** | Docker & LocalStack |
| **Infraestrutura como Código** | AWS CDK (Python) |
| **Computação em Nuvem (Backend)** | AWS Lambda (Python 3.9) |
| **Banco de Dados** | Amazon DynamoDB (NoSQL) |
| **Gerenciamento de API** | Amazon API Gateway |
| **Segurança e Permissões** | AWS IAM |
| **Front-end** | HTML5, CSS3, JavaScript (Vanilla) |

---
🌐 **Como executar (Replicação):**

**Pré-requisitos:** Git, Docker, Docker Compose, Node.js, Python 3.9+ e `aws-cdk-local` (`npm install -g aws-cdk-local`).

1. Abra o **Git Bash** e clone o repositório:
```bash
git clone https://github.com/beatrisAS/TCC_AWS_contador_acessos.git
cd TCC_AWS_contador_acessos
```

2. Inicie a "Mini Nuvem" (LocalStack):
```bash
docker-compose up -d
```

3. Faça o deploy da infraestrutura (Backend):
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # No Windows use: .venv\Scripts\activate
pip install -r requirements.txt
cdklocal bootstrap
cdklocal deploy
```
*(Ao fim deste processo, o terminal mostrará a URL do API Gateway simulado. Copie-a).*

4. Configure e execute o Front-end:
```bash
cd ../frontend
```
- Abra o arquivo `script.js` e substitua a constante/variável da URL pela que você copiou.
- Dê um duplo clique no arquivo `index.html` para abri-lo diretamente no seu navegador.
- Pressione F5 ou atualize a página para simular o incremento de acessos (fazendo a requisição real para o Lambda + DynamoDB rodando no seu Docker).

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
