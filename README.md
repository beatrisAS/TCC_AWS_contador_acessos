# Contador de Acessos Serverless

Projeto conceitual desenvolvido para o TCC da Escola da Nuvem, baseado no repositório de referência [tcc-contador-acessos](https://github.com/craffos/tcc-contador-acessos).

## Objetivo

Simular uma solução de contador de acessos para uma landing page de produto. Na arquitetura planejada, o usuário acessa a página, o API Gateway recebe a requisição, a AWS Lambda processa o evento e o DynamoDB armazena o total.

> Este projeto foi preparado para ser apresentado sem acesso a uma conta AWS. A pasta `local/` permite testar o comportamento do contador no computador. A pasta raiz contém também a infraestrutura AWS CDK planejada, que pode ser sintetizada quando o CDK estiver disponível, mas não precisa ser implantada para a apresentação.

## Arquitetura planejada

```text
Usuário -> CloudFront/S3 -> API Gateway -> Lambda -> DynamoDB
                                      |
                              IAM e CloudWatch
```

Os arquivos `clickops_stack.py` e `app.py` representam a infraestrutura em AWS CDK, seguindo a organização do repositório de referência. A função `lambda/contador.py` contém a lógica planejada para atualizar o item `id = hits` no DynamoDB.

## Como testar localmente

É necessário ter Python 3.10 ou superior instalado.

```bash
cd contador-acessos-serverless
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python local/server.py
```

Depois, abra `http://127.0.0.1:5000` no navegador e clique em **Tenho interesse**. O total será salvo localmente em `local/counter.txt`, simulando a persistência do DynamoDB.

Também é possível testar a API pelo terminal:

```bash
curl http://127.0.0.1:5000/hits
curl -X POST http://127.0.0.1:5000/hits
curl -X POST http://127.0.0.1:5000/hits
curl -X POST http://127.0.0.1:5000/reset
```

## Testes automatizados

Com o ambiente virtual ativado, execute:

```bash
pytest -q
```

## Síntese do CDK, sem deploy

Se o AWS CDK estiver instalado, a infraestrutura pode ser validada sem criar recursos na AWS:

```bash
cdk synth
```

O comando `cdk synth` apenas gera o template CloudFormation. O projeto não deve executar `cdk deploy` sem autorização, conta AWS e controle de custos.

## Estrutura

```text
contador-acessos-serverless/
├── README.md
├── app.py
├── clickops_stack.py
├── requirements.txt
├── lambda/
│   └── contador.py
├── local/
│   └── server.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── tests/
│   └── test_local_server.py
└── docs/
    └── cenarios-simulados.md
```

## Limitações conhecidas

A simulação local não chama API Gateway, Lambda ou DynamoDB reais. Ela usa Flask e um arquivo de texto para representar o fluxo. A infraestrutura CDK é a representação do ambiente que seria criado em uma conta AWS. Na apresentação, essa diferença deve ser informada com transparência.

A tabela DynamoDB está configurada com `RemovalPolicy.DESTROY` para facilitar um eventual ambiente de laboratório. Em uma aplicação real, seria necessário avaliar uma política de retenção mais segura.

## Publicação no GitHub

Crie um repositório vazio no GitHub e execute:

```bash
git init
git add .
git commit -m "feat: contador de acessos serverless conceitual"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/contador-acessos-serverless.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo usuário do GitHub e mantenha o repositório sem credenciais, tokens ou arquivos `.env`.

## Referência

O desenho foi baseado no repositório público [craffos/tcc-contador-acessos](https://github.com/craffos/tcc-contador-acessos), que utiliza Python, AWS CDK, API Gateway, Lambda, DynamoDB, S3, CloudFront e WAF.
