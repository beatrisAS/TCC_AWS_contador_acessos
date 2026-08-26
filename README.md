# Contador de Acessos Serverless

> **Uma arquitetura Serverless para registrar acessos em páginas de lançamento.**

O Contador de Acessos é uma solução Serverless para páginas de lançamento e campanhas de marketing que precisam medir quantas pessoas demonstraram interesse em um produto. A proposta é simples para o usuário final: acessar uma landing page e registrar um interesse. Por trás dessa experiência, uma arquitetura orientada a eventos recebe a chamada, processa o incremento e persiste o total.

Este repositório contém a aplicação demonstrável, a infraestrutura como código e duas formas de validação. A execução recomendada usa uma API Python offline e não exige Docker, LocalStack, conta externa ou credenciais. O LocalStack permanece documentado como alternativa opcional para quem desejar emular serviços AWS. O deploy em uma conta AWS real é uma etapa futura e deve ser realizado somente após revisão de custos, permissões e segurança.

## Problema que a aplicação resolve

Uma campanha de lançamento precisa medir rapidamente o interesse do público, mas não conhece o volume de tráfego antes de divulgar a página. Uma solução tradicional exigiria manter servidor e banco dimensionados antecipadamente, mesmo quando a campanha estiver ociosa. Em um pico, o dimensionamento insuficiente pode comprometer a disponibilidade e a qualidade do dado.

A aplicação endereça essa necessidade com uma arquitetura que separa apresentação, processamento e persistência. O sistema registra cada chamada sem depender de um servidor permanente e mantém o contador em um item único do DynamoDB.

## Objetivo da aplicação

| Necessidade do negócio | Resposta da aplicação |
|---|---|
| Medir interesse em uma campanha | Endpoint `GET /acessos` integrado à landing page |
| Lidar com tráfego imprevisível | AWS Lambda e serviços gerenciados sob demanda |
| Evitar perda ou conflito no total | Atualização atômica com `ADD acessos :inc` |
| Controlar custo e operação | Arquitetura Serverless e estimativa pela AWS Pricing Calculator |
| Validar sem conta AWS | Docker + LocalStack + `cdklocal` |

## Como funciona

```text
Usuário
   |
   v
Landing page estática
   |
   v
Amazon API Gateway  —  GET /acessos
   |
   v
AWS Lambda  —  incrementa o contador
   |
   v
Amazon DynamoDB  —  id = hits
```

O usuário acessa a página e o front-end chama o endpoint. O API Gateway encaminha o evento para a Lambda. A função executa `UpdateItem` com a expressão `ADD acessos :inc`, recebendo o novo valor no retorno da operação. O total é devolvido em JSON para ser exibido pela interface.

## Serviços AWS e justificativas

| Serviço | O que é | Uso no produto | Por que foi escolhido |
|---|---|---|---|
| **Amazon API Gateway** | Serviço gerenciado para criação e publicação de APIs HTTP/REST. | Expõe o recurso `/acessos` e encaminha requisições para a Lambda. | Integração direta com front-end, controle de acesso e operação sem servidor dedicado. |
| **AWS Lambda** | Computação Serverless que executa código em resposta a eventos. | Processa o evento e incrementa o contador. | Executa sob demanda, reduz operação contínua e acompanha variações de tráfego. |
| **Amazon DynamoDB** | Banco NoSQL gerenciado para dados de baixa latência e escala. | Persiste o item global do contador. | Modelo simples, operação atômica e integração nativa com IAM e Lambda. |
| **Amazon S3** | Armazenamento de objetos. | Hospedaria os arquivos estáticos em uma implantação real. | Adequado para HTML, CSS e JavaScript de uma landing page. |
| **Amazon CloudFront** | Rede de distribuição de conteúdo. | Entregaria a página com menor latência em diferentes regiões. | Complementa o S3 e melhora a distribuição do conteúdo estático. |
| **AWS IAM** | Serviço de identidades e políticas de acesso. | Controla a role da Lambda. | Permite aplicar o princípio do menor privilégio. |
| **Amazon CloudWatch** | Monitoramento, métricas e logs operacionais. | Acompanharia invocações, falhas e latência. | Dá visibilidade para operar a solução em produção. |

## Decisões técnicas

O requisito central era registrar acessos com volume desconhecido e baixa complexidade de domínio. Foram consideradas duas alternativas: um servidor tradicional com banco relacional e uma arquitetura Serverless com banco gerenciado. A primeira opção aumentaria a responsabilidade de operação e exigiria planejamento de capacidade. A segunda foi escolhida porque combina execução sob demanda, integração entre serviços, escalabilidade e familiaridade da equipe.

O contador utiliza uma chave fixa `id = hits` porque o escopo inicial mede um total único. Caso o produto evolua para múltiplas campanhas, a chave poderá ser composta por campanha, período ou produto. A atualização é feita diretamente no DynamoDB para evitar o padrão concorrente de ler o valor, somar na aplicação e gravar novamente.

## Escalabilidade, resiliência e segurança

**Escalabilidade.** O API Gateway e o Lambda são serviços gerenciados e orientados a eventos. O DynamoDB utiliza modo de cobrança sob demanda no CDK, adequado quando o volume de requisições ainda é incerto. Com dez vezes mais usuários, o desenho não exige ligar novos servidores manualmente; a capacidade é administrada pelos serviços, respeitando limites e cotas que devem ser revisados em produção.

**Resiliência.** A solução evita estado local na função e mantém o dado no DynamoDB. Em uma implantação real, a disponibilidade dos serviços gerenciados, a distribuição do conteúdo via CloudFront e alarmes no CloudWatch seriam validados com testes de falha e critérios de recuperação. O LocalStack é usado para validar o fluxo, mas não substitui testes de disponibilidade na AWS oficial.

**Segurança.** A Lambda recebe uma role própria e acesso somente à tabela do contador por meio de `grant_read_write_data`. O repositório não contém credenciais reais. Para produção, recomenda-se restringir CORS às origens necessárias, usar HTTPS via CloudFront, considerar AWS WAF e revisar logs para evitar dados sensíveis.

## Custos e uso consciente da AWS

O projeto não apresenta um valor mensal inventado porque não foi executado em uma conta AWS real. A estimativa de produção deve ser calculada na [AWS Pricing Calculator](https://calculator.aws/) a partir de premissas documentadas: número de acessos, chamadas ao API Gateway, duração das funções Lambda, armazenamento no DynamoDB e volume de distribuição pelo CloudFront.

A estratégia de custo é priorizar serviços sob demanda, verificar o Free Tier vigente e configurar alertas de billing antes do deploy. O LocalStack permite desenvolver e demonstrar o fluxo sem consumir recursos da conta AWS, mas não representa uma fatura AWS nem substitui a validação oficial de preços.

## Execução offline — recomendada para a demonstração

Esta é a forma principal de executar o contador. Ela usa uma API Flask local e o arquivo `local/data.json` como persistência, reproduzindo o comportamento da Lambda e do item `id = hits` sem depender de serviços externos.

### Instalação

No PowerShell do VS Code:

```powershell
cd C:\Users\beatr\Downloads\TCC_AWS_contador_acessos\contador-de-acessos-aws
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\local\requirements.txt
```

Se o PowerShell bloquear a ativação do ambiente, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Iniciar a API local

Em um terminal:

```powershell
python .\local\server.py
```

A API ficará disponível em `http://127.0.0.1:5000`.

### Iniciar a interface

Abra um segundo terminal do VS Code:

```powershell
cd C:\Users\beatr\Downloads\TCC_AWS_contador_acessos\contador-de-acessos-aws\frontend
python -m http.server 8080
```

Abra `http://localhost:8080`, clique em **Registrar meu acesso** e observe o total. Para testar a API diretamente:

```powershell
curl.exe http://127.0.0.1:5000/api/health
curl.exe http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/acessos
```

O arquivo `local/data.json` será criado automaticamente. Para zerar o contador:

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/reset
```

A arquitetura AWS correspondente continua sendo: `API Gateway → Lambda → DynamoDB`. Nesta execução, as três camadas são representadas por `server.py`, suas funções de incremento e `data.json`.

## Execução opcional com LocalStack

### Pré-requisitos

Instale Docker Desktop, Python 3.10 ou superior, Node.js/npm, Git e, opcionalmente, AWS CLI. O projeto usa credenciais fictícias do LocalStack: `AWS_ACCESS_KEY_ID=test`, `AWS_SECRET_ACCESS_KEY=test` e conta `000000000000`.

### Iniciar a nuvem local

```bash
git clone https://github.com/beatrisAS/TCC_AWS_contador_acessos.git
cd TCC_AWS_contador_acessos
docker compose up -d
curl http://localhost:4566/_localstack/health
```

### Instalar e executar o CDK local

```bash
npm install -g aws-cdk aws-cdk-local
cd contador-de-acessos-aws/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export CDK_DEFAULT_ACCOUNT=000000000000
export CDK_DEFAULT_REGION=us-east-1
cdklocal bootstrap
cdklocal deploy --require-approval never
```

No Windows PowerShell, use `.venv\\Scripts\\Activate.ps1` e substitua `export NOME=valor` por `$env:NOME="valor"`.

O deploy informa a URL local do API Gateway. Copie essa URL para `contador-de-acessos-aws/frontend/config.js`:

```javascript
window.CONTADOR_API_URL = "http://localhost:4566/restapis/ID_DO_API/local/_user_request_/acessos";
```

Depois, sirva o front-end:

```bash
cd contador-de-acessos-aws/frontend
python3 -m http.server 8080
```

Acesse `http://localhost:8080` e registre acessos pela interface. Se a URL estiver vazia ou indisponível, o front-end utiliza o fallback local com `localStorage` e informa o modo de demonstração.

## LocalStack opcional

A configuração Docker/LocalStack continua disponível em `contador-de-acessos-aws/docker-compose.yml`. Ela exige um token do LocalStack na imagem atual e não é necessária para testar a aplicação. Para a apresentação sem cadastro e sem custos, utilize a execução offline descrita acima.

## Validação

O roteiro completo está em [`docs/testes-localstack.md`](docs/testes-localstack.md). A validação principal consiste em confirmar a saúde do LocalStack, chamar o endpoint duas vezes e observar a sequência `total_acessos: 1` e `total_acessos: 2`. Em seguida, a tabela pode ser consultada no DynamoDB local para confirmar a persistência do item `id = hits`.

## Replicação: qualquer pessoa consegue executar?

O repositório foi organizado para ser reproduzido por outra pessoa sem depender de explicações privadas. O README registra pré-requisitos, comandos, variáveis de ambiente e limitações. O `docker-compose.yml` define o ambiente local, o AWS CDK define a infraestrutura, `scripts/setup-local.sh` automatiza a preparação e `docs/testes-localstack.md` documenta a validação.

Nenhuma credencial real deve ser colocada em `config.js`, no código ou no histórico Git. Antes de compartilhar uma URL da API, confirme que ela aponta para o ambiente local ou para um endpoint autorizado.

## Diferencial e aplicação real

O contador resolve um problema reconhecível de marketing: transformar acessos em um sinal mensurável de interesse durante uma campanha. A proposta combina uma experiência simples para o usuário com uma arquitetura que pode evoluir para múltiplas campanhas, dashboard, autenticação administrativa, alertas e implantação com domínio, HTTPS e monitoramento.

O resultado é um produto pequeno, mas completo como referência de engenharia: tem uma interface, um contrato de API, uma função de negócio, persistência, permissões, infraestrutura como código, ambiente de teste local e documentação de reprodução.

## Estrutura do repositório

```text
.
├── contador-de-acessos-aws/
│   ├── backend/
│   │   ├── app.py
│   │   ├── contador_acessos/contador_stack.py
│   │   ├── lambda/contador_lambda.py
│   │   └── requirements.txt
│   └── frontend/
│       ├── index.html
│       ├── script.js
│       └── config.js
├── docs/testes-localstack.md
├── scripts/setup-local.sh
├── docker-compose.yml
└── README.md
```

## Limitações

Este repositório foi preparado para fins acadêmicos e validação local. O LocalStack não é uma conta AWS real e pode ter diferenças ou limitações em relação aos serviços oficiais. O comando `cdk deploy` não deve ser executado sem autorização, orçamento e revisão das políticas; para a simulação, utilize `cdklocal deploy`.

## Referências

[1]: https://aws.amazon.com/lambda/ "AWS Lambda — página oficial"
[2]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scenario_AtomicCounterOperations_section.html "DynamoDB — contadores atômicos"
[3]: https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html "Amazon API Gateway — documentação oficial"
[4]: https://docs.localstack.cloud/aws/connecting/infrastructure-as-code/aws-cdk/ "LocalStack — integração com AWS CDK"
[5]: https://calculator.aws/ "AWS Pricing Calculator"

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