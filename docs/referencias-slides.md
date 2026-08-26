# Referências técnicas para os slides

## Pontos confirmados

A AWS descreve o Lambda como um serviço de computação Serverless que executa código em resposta a eventos, sem provisionamento ou gerenciamento de servidores. A página oficial também destaca execução orientada a eventos, escalabilidade automática e cobrança por uso.

A documentação do DynamoDB apresenta operações de contador atômico com `ADD` e `SET`. Isso embasa a escolha do projeto por `UpdateExpression='ADD acessos :inc'` para incrementar o item `id = hits`.

A documentação do API Gateway define o serviço como a porta de entrada para criar, publicar, monitorar e proteger APIs REST, HTTP e WebSocket. No projeto, o API Gateway expõe o recurso `/acessos` e integra a chamada com a Lambda.

A documentação do LocalStack informa que `cdklocal` é um wrapper do CDK para direcionar a infraestrutura às APIs locais do LocalStack. A configuração recomendada usa `docker compose`, `cdklocal bootstrap` e `cdklocal deploy`. A documentação também alerta que recursos de asset deployment do CDK podem ter limitações conforme o plano do LocalStack.

## URLs

[1]: https://aws.amazon.com/lambda/ "AWS Lambda — página oficial"
[2]: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/example_dynamodb_Scenario_AtomicCounterOperations_section.html "DynamoDB — operações de contador atômico"
[3]: https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html "Amazon API Gateway — documentação oficial"
[4]: https://docs.localstack.cloud/aws/connecting/infrastructure-as-code/aws-cdk/ "LocalStack — integração com AWS CDK"
[5]: https://github.com/beatrisAS/TCC_AWS_contador_acessos "Repositório do projeto do grupo"
