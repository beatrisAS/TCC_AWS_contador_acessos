# Contador de Acessos Serverless

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-API_local-000000?logo=flask&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-arquitetura_conceitual-FF9900?logo=amazonaws&logoColor=white) ![CDK](https://img.shields.io/badge/AWS_CDK-Infrastructure_as_Code-FF9900?logo=amazonaws&logoColor=white) ![License](https://img.shields.io/badge/uso-acadêmico-2EA44F)

> **Uma aplicação para registrar acessos em páginas de lançamento.**

## Visão Geral

Uma campanha de lançamento precisa medir rapidamente quantas pessoas chegaram à sua página. O volume de acessos pode variar bastante e, antes da divulgação, não é possível saber se haverá poucos visitantes ou um pico de tráfego.

Este projeto apresenta um contador de acessos com uma interface simples e uma arquitetura planejada para execução sob demanda. A versão disponível neste repositório roda totalmente no computador, sem conta AWS, sem credenciais, sem Docker e sem serviços externos. Assim, o grupo consegue testar e apresentar o comportamento da aplicação sem risco de cobrança.

## 🎯 Objetivo da aplicação

A aplicação registra cada solicitação de interesse e mostra o total atualizado. O usuário acessa a página e seleciona **Registrar meu acesso**. A API local recebe a chamada, incrementa o valor e salva o resultado em um arquivo JSON.

Na arquitetura planejada para produção, o mesmo fluxo seria implementado por **Amazon API Gateway**, **AWS Lambda** e **Amazon DynamoDB**. A execução local é uma representação funcional desse fluxo, não um deploy real na AWS.

## 🔄 Fluxo da solução

```text
Usuário
   |
   v
Página HTML estática
   |
   v
API local — GET/POST /api/acessos
   |
   v
Função de incremento
   |
   v
Arquivo local/data.json — id = hits
```

Correspondência conceitual com a AWS:

```text
Página estática  →  Amazon S3 / CloudFront
API local        →  Amazon API Gateway
Função de incremento → AWS Lambda
local/data.json  →  Amazon DynamoDB
```

## 🗂️ Estrutura do repositório

```text
.
├── contador-de-acessos-aws/
│   ├── backend/
│   │   ├── app.py
│   │   ├── contador_acessos/contador_stack.py
│   │   ├── lambda/contador_lambda.py
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html
│   │   ├── script.js
│   │   └── config.js
│   └── local/
│       ├── server.py
│       ├── test_server.py
│       └── requirements.txt
├── docs/testes-offline.md
├── README.md
└── .gitignore
```

## 🧰 Pré-requisitos

Para executar a demonstração, instale apenas **Python 3.10 ou superior**. O projeto não exige conta AWS, cartão, credenciais, Docker ou conexão com serviços em nuvem.

## ▶️ Como executar no Windows

Abra o terminal integrado do VS Code e entre na pasta do projeto:

```powershell
cd C:\Users\beatr\Downloads\TCC_AWS_contador_acessos\contador-de-acessos-aws
```

Crie um ambiente virtual, ative-o e instale a dependência local:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\local\requirements.txt
```

Se o PowerShell bloquear a ativação, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Em um primeiro terminal, inicie a API:

```powershell
python .\local\server.py
```

A API ficará disponível em `http://127.0.0.1:5000`.

Abra um segundo terminal e inicie a página:

```powershell
cd C:\Users\beatr\Downloads\TCC_AWS_contador_acessos\contador-de-acessos-aws\frontend
python -m http.server 8080
```

Acesse `http://localhost:8080`. Clique em **Registrar meu acesso** e observe o total. A API grava o valor em `local/data.json`, que é criado automaticamente na primeira chamada.

## 🧪 Testar a API diretamente

Use um terceiro terminal para verificar a saúde da aplicação e consultar ou alterar o contador:

```powershell
curl.exe http://127.0.0.1:5000/api/health
curl.exe http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/reset
```

A chamada `POST /api/acessos` incrementa o total em uma unidade. A chamada `POST /api/reset` retorna o valor para zero.

## ✅ Testes automatizados

Na pasta `contador-de-acessos-aws/local`, execute:

```powershell
pip install pytest
python -m pytest -q
```

Os testes verificam a saúde da API, a consulta inicial, o incremento, a persistência em JSON e o reset do contador.

## ⚙️ Decisões técnicas

O contador usa a identificação fixa `id = hits` porque o escopo atual mede um total único. O incremento ocorre antes da gravação, evitando que a aplicação dependa de uma leitura e uma escrita separadas para calcular o próximo valor.

Na arquitetura AWS, essa decisão seria implementada por uma atualização atômica no DynamoDB, por meio de `UpdateItem` e da expressão `ADD acessos :inc`. A função Lambda teria uma role IAM com acesso somente à tabela necessária, aplicando o princípio do menor privilégio.

## 📈 Escalabilidade e segurança planejadas

A arquitetura AWS foi escolhida porque API Gateway e Lambda podem receber requisições sob demanda, enquanto o DynamoDB oferece uma persistência gerenciada adequada ao contador. Em uma implantação real, seriam revisadas cotas, limites, CORS, HTTPS, logs, alarmes, WAF e permissões IAM.

A versão offline não representa disponibilidade de produção, escalabilidade real nem custos da AWS. Ela serve para demonstrar a regra de negócio, o contrato da API e a experiência da página sem depender de uma conta em nuvem.

## 💰 Custos

Nenhum recurso AWS é criado durante a execução descrita neste README. Por isso, a demonstração não gera cobrança. Se o projeto for levado para a AWS no futuro, o custo deverá ser calculado com premissas explícitas de acessos, chamadas, duração de funções, armazenamento e distribuição de conteúdo.

## ⚠️ Limitações

O armazenamento em `local/data.json` é adequado para uma demonstração individual, mas não substitui um banco distribuído. A API Flask local também não substitui os serviços gerenciados da AWS. Essas limitações devem ser apresentadas claramente durante a defesa.

## 👥 Integrantes

O projeto foi desenvolvido por **Alexandra Prudencio Domiciano**, **Beatris Antunes Silva**, **Deivid Marcio Dos Santos Ferreira**, **Guilherme José Rodrigues Filho**, **Rafael De Matos Correa Figueiredo** e **William Dos Santos Martins**.

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e educacionais no âmbito do programa **AWS re/Start · Escola da Nuvem · 2026**.

## 🔗 Referências


[1]: https://github.com/craffos/tcc-contador-acessos "Repositório de referência do contador de acessos"
[2]: https://github.com/beatrisAS/TCC_AWS_contador_acessos "Repositório do projeto"
[3]: https://aws.amazon.com/lambda/ "AWS Lambda — página oficial"
[4]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scenario_AtomicCounterOperations_section.html "DynamoDB — contadores atômicos"
[5]: https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html "Amazon API Gateway — documentação oficial"
