# 🚀 Contador de Acessos Serverless

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-FF9900?logo=amazonaws&logoColor=white) ![CDK](https://img.shields.io/badge/AWS_CDK-IaC-FF9900?logo=amazonaws&logoColor=white) ![License](https://img.shields.io/badge/uso-acadêmico-2EA44F)

> **Uma aplicação para registrar acessos em páginas de lançamento.**

## 📋 **Sobre o produto**

Uma startup está lançando um novo produto e precisa medir, de forma objetiva, quantas pessoas demonstraram interesse em uma página de “Em Breve”. O desafio é que a campanha pode receber poucos acessos ou um pico expressivo de tráfego, sem que a equipe precise manter servidores ligados permanentemente.

O **Contador de Acessos Serverless** transforma cada interação em uma métrica de interesse. O usuário realiza uma ação na página, o evento é processado e o total atualizado fica disponível para acompanhamento. A proposta combina uma interface de baixa fricção com uma arquitetura Serverless planejada para reduzir operação manual e acompanhar a demanda.

## 🎯 **Problema e oportunidade**

Sem uma solução dedicada, a campanha depende de contagens manuais, métricas dispersas ou uma infraestrutura dimensionada por estimativa. Subdimensionar pode causar indisponibilidade; superdimensionar pode gerar recursos ociosos.

A solução proposta concentra o problema em um fluxo pequeno e mensurável: receber a interação, incrementar um contador global e devolver o resultado atualizado. Esse recorte é adequado para uma campanha inicial porque oferece um indicador claro de interesse sem adicionar complexidade desnecessária à experiência.

## 💡 **Proposta de valor**

O produto entrega uma forma direta de responder à pergunta **“quantas pessoas chegaram até aqui?”**. Para o negócio, isso significa uma métrica inicial de demanda. Para a equipe técnica, significa uma base simples, documentada e preparada para evoluir para serviços gerenciados da AWS.

A demonstração local deste repositório permite validar o comportamento sem conta AWS, sem credenciais e sem custos. A arquitetura de produção é apresentada separadamente como desenho conceitual, preservando a distinção entre o que foi executado e o que foi planejado.

## 🏗️ **Arquitetura e decisões técnicas**

O projeto foi organizado em três responsabilidades principais:

| Camada | Implementação local | Serviço AWS planejado | Decisão |
| :--- | :--- | :--- | :--- |
| Acesso | Front-end HTML e JavaScript | Amazon API Gateway | Centraliza a entrada das requisições. |
| Processamento | API local e regra de incremento | AWS Lambda | Executa a lógica sob demanda. |
| Dados | Arquivo JSON persistente | Amazon DynamoDB | Armazena o item global `id = hits`. |
| Segurança | CORS controlado para a demonstração | AWS IAM | Limita a função às ações necessárias na tabela. |

Na versão AWS, a Lambda usaria uma atualização atômica com `UpdateItem` e `ADD acessos :inc`, evitando a separação insegura entre ler o valor e gravar o próximo valor. A tabela teria uma partition key fixa, `id`, com o item `hits` representando o total global.

## 🔄 **Fluxo do produto**

```text
Usuário seleciona “Registrar acesso”
              ↓
Front-end envia POST /api/acessos
              ↓
Regra de negócio incrementa o contador
              ↓
Total é persistido e devolvido à interface
```

Correspondência com a arquitetura planejada:

```text
Página estática → API Gateway → AWS Lambda → DynamoDB
                                             └→ IAM
```

## ✨ **Funcionalidades**

- Contagem global de acessos com identificador `hits`.
- Consulta do total atual por `GET /api/acessos`.
- Registro de um novo acesso por `POST /api/acessos`.
- Reinício do contador por `POST /api/reset`.
- Endpoint de saúde em `GET /api/health`.
- Persistência local em JSON para repetir a demonstração sem perder o valor ao recarregar a API.
- Função Lambda e stack CDK incluídas como base da arquitetura AWS.
- Testes automatizados para o fluxo principal.

## 🛠️ **Tecnologias**

| Área | Tecnologia | Uso no projeto |
| :--- | :--- | :--- |
| Interface | HTML5, CSS básico e JavaScript | Página de demonstração e chamadas HTTP. |
| API local | Python e Flask | Simulação executável da entrada e do processamento. |
| Persistência local | JSON | Armazenamento simples para a demonstração. |
| Computação planejada | AWS Lambda | Função orientada a eventos. |
| Banco planejado | Amazon DynamoDB | Persistência NoSQL do contador. |
| API planejada | Amazon API Gateway | Porta de entrada da aplicação. |
| Infraestrutura planejada | AWS CDK em Python | Definição da infraestrutura como código. |
| Segurança planejada | AWS IAM | Controle de permissões da função. |

## ▶️ **Como executar a demonstração**

### Pré-requisitos

É necessário ter Python 3.10 ou superior. A execução demonstrativa não exige conta AWS, credenciais ou serviços externos.

### **API local**

No terminal integrado do VS Code, na raiz do projeto, execute:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python .\local_api\server.py
```

A API ficará disponível em `http://127.0.0.1:5000`.

### **Front-end**

Abra um segundo terminal na raiz do projeto e execute:

```powershell
python -m http.server 8080 --directory frontend
```

Acesse `http://localhost:8080` e selecione **Registrar acesso**. A página consultará a API, exibirá o total e atualizará o valor após cada interação.

### **Testes da API**

Com as dependências instaladas, execute:

```powershell
python -m pytest -q
```

Também é possível testar manualmente:

```powershell
curl.exe http://127.0.0.1:5000/api/health
curl.exe http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/reset
```

## 📈 **Escalabilidade, segurança e custos**

A arquitetura AWS foi escolhida para que o processamento acompanhe a demanda sem manter uma instância de servidor permanentemente ativa. Em produção, a solução precisaria ser submetida a testes de carga, definição de limites, configuração de CORS, HTTPS, logs e alarmes.

A Lambda deveria receber apenas a permissão de leitura e escrita necessária na tabela do contador. O acesso amplo a outros recursos não faz parte da proposta. A estimativa de custos dependeria de acessos, quantidade de chamadas, duração das funções, armazenamento e distribuição da página; por isso, este repositório não apresenta valores inventados.

## 🧪 **Escopo da validação**

A execução local valida o contrato da API, a regra de incremento, a persistência do valor e a interação básica do front-end. Ela não comprova escalabilidade, disponibilidade ou custos de uma implantação real na AWS. Essa distinção deve ser mantida na defesa para apresentar o produto com precisão técnica.


## 👥 **Equipe**

- Alexandra Prudencio Domiciano
- Beatris Antunes Silva
- Deivid Marcio Dos Santos Ferreira
- Guilherme José Rodrigues Filho
- Rafael De Matos Correa Figueiredo
- William Dos Santos Martins.

## 📄 **Licença**

Este projeto foi desenvolvido para fins acadêmicos e educacionais no âmbito do programa **AWS re/Start · Escola da Nuvem · 2026**.
