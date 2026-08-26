# Defesa do TCC — Contador de Acessos Serverless

## Cover
Contador de Acessos Serverless
Uma arquitetura AWS para medir interesse em uma campanha de lançamento
TCC · Escola da Nuvem · Equipe ClickOps

## Slide 1
Uma campanha precisa transformar interesse em evidência
- A startup criou uma página “Em Breve” para um novo produto.
- O objetivo é registrar acessos ou cliques de interesse.
- O tráfego é imprevisível: pode começar pequeno e crescer rapidamente.
- A métrica precisa ser simples, persistente e acessível.

## Slide 2
O desafio é escalar sem manter um servidor ligado
- Servidores tradicionais exigem capacidade planejada e manutenção.
- Um pico de acessos pode gerar gargalos ou custo de ociosidade.
- A arquitetura escolhida executa componentes sob demanda.
- O critério principal foi combinar simplicidade, escala e baixo custo operacional.

## Slide 3
A solução separa entrada, processamento e dados
- API Gateway funciona como porta de entrada da requisição.
- AWS Lambda executa a lógica do contador quando acionada.
- DynamoDB armazena o total no item com `id = hits`.
- S3/CloudFront entregam a página; IAM e CloudWatch apoiam segurança e operação.

## Slide 4
O dado percorre um fluxo curto e rastreável
- Usuário acessa a página estática.
- Front-end chama `GET /acessos`.
- API Gateway encaminha para a Lambda.
- Lambda executa `ADD acessos :inc` no DynamoDB e retorna o total.

## Slide 5
A atualização atômica protege o contador
- Tabela: contador de acessos.
- Partition Key: `id`.
- Item global: `{ "id": "hits", "acessos": N }`.
- A operação `ADD` incrementa diretamente no banco.
- A escolha evita o padrão frágil “ler → somar no código → gravar”.

## Slide 6
O CDK transforma a arquitetura em código reproduzível
- `contador_stack.py` define DynamoDB, Lambda, API Gateway e IAM.
- `app.py` inicializa o stack em Python.
- A role da Lambda recebe acesso de leitura e escrita na tabela.
- O mesmo desenho pode ser direcionado ao LocalStack com `cdklocal`.

## Slide 7
LocalStack permite validar sem conta AWS
- Docker executa uma nuvem AWS simulada localmente.
- `docker compose up -d` inicia os serviços necessários.
- `cdklocal bootstrap` prepara o ambiente.
- `cdklocal deploy` cria os recursos no LocalStack, não na conta real.
- A solução também mantém fallback com `localStorage` para uma demonstração simples.

## Slide 8
O repositório passou a ser executável e documentado
- `docker-compose.yml`: ambiente local.
- `scripts/setup-local.sh`: preparação e deploy local.
- `frontend/config.js`: URL da API sem credenciais.
- `docs/testes-localstack.md`: comandos de validação.
- README: instalação, execução, limpeza e limitações.

## Slide 9
A validação combina API, banco e front-end
- Saúde do ambiente: `curl http://localhost:4566/_localstack/health`.
- API: chamadas consecutivas ao endpoint `/acessos`.
- Resultado esperado: `total_acessos` evolui de 1 para 2, 3 e assim por diante.
- Banco: consulta da tabela local com AWS CLI ou `awslocal`.
- Interface: contador exibe o valor retornado pelo fluxo.

## Slide 10
Segurança e operação foram consideradas desde o desenho
- IAM aplica o princípio do menor privilégio.
- Credenciais reais não entram no código ou no GitHub.
- CORS permite a comunicação controlada entre front-end e API.
- CloudWatch é a camada planejada para logs e métricas.
- WAF, HTTPS e CloudFront são camadas complementares para uma implantação real.

## Slide 11
Conclusão: o projeto demonstra o ciclo completo
- O problema de negócio foi traduzido em uma arquitetura Serverless objetiva.
- O contador usa uma atualização atômica e um modelo de dados simples.
- O CDK documenta a infraestrutura como código.
- O LocalStack permite testar sem custos de uma conta AWS.
- A equipe entrega uma solução reproduzível, transparente e pronta para evolução.

## Slide 12
Próximas evoluções
- Separar contadores por campanha ou produto.
- Adicionar dashboard de acessos por período.
- Criar autenticação para uma área administrativa.
- Monitorar erros e configurar alertas de operação.
- Migrar do ambiente local para AWS após validação de custos e permissões.

Referências
[1] Projeto do grupo: https://github.com/beatrisAS/TCC_AWS_contador_acessos
[2] Repositório de referência: https://github.com/craffos/tcc-contador-acessos
[3] AWS Lambda: https://aws.amazon.com/lambda/
[4] DynamoDB — contadores atômicos: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scenario_AtomicCounterOperations_section.html
[5] API Gateway: https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html
[6] LocalStack + CDK: https://docs.localstack.cloud/aws/connecting/infrastructure-as-code/aws-cdk/
