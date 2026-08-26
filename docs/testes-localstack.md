# Testes no LocalStack

## Saúde do ambiente

```bash
curl http://localhost:4566/_localstack/health
```

## Encontrar a URL do API Gateway

Após o `cdklocal deploy`, procure o output do stack. A URL termina em `/acessos`.

```bash
curl "http://localhost:4566/restapis/ID_DO_API/local/_user_request_/acessos"
```

## Sequência esperada

A primeira chamada deve retornar `total_acessos: 1`. A segunda deve retornar `total_acessos: 2`. O incremento ocorre na Lambda e é persistido na tabela DynamoDB local.

## Consultar a tabela

```bash
aws --endpoint-url=http://localhost:4566 dynamodb list-tables --region us-east-1
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name NOME_DA_TABELA --region us-east-1
```

## Testar a Lambda sem API Gateway

```bash
aws --endpoint-url=http://localhost:4566 lambda list-functions --region us-east-1
```

## Limpeza

```bash
docker compose down -v
```

O LocalStack é apenas uma simulação local. Os resultados não são recursos criados em uma conta AWS real.
