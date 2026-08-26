# Cenários simulados — Contador de Acessos

## Objetivo

Estes cenários servem exclusivamente para demonstrar o comportamento esperado da solução. Eles não representam dados coletados em uma conta AWS real.

| Cenário | Requisições recebidas | Valor esperado do contador |
|---|---:|---:|
| Estado inicial | 0 | 0 |
| Primeiro acesso | 1 | 1 |
| Segunda chamada | 1 | 2 |
| Dez novos acessos | 10 | 12 |
| Nova campanha com contador reiniciado | 0 | 0 |

## Exemplo de entrada conceitual

```json
{
  "httpMethod": "POST",
  "path": "/hits",
  "body": null
}
```

## Exemplo de resposta conceitual

```json
{
  "statusCode": 200,
  "body": {
    "message": "Acesso registrado com sucesso",
    "total": 12
  }
}
```

## Roteiro da demonstração

A equipe deve iniciar informando que o contador está em zero. Em seguida, deve apresentar uma chamada simulada ao endpoint. O resultado esperado é o valor um. Após mais duas chamadas, o total esperado é três. Para representar um volume maior de acessos, a equipe pode informar que dez novas requisições foram processadas e que o contador chegaria a treze.

Durante a explicação, deve ser reforçado que, em uma implantação real, a requisição seria recebida pelo API Gateway, processada pela Lambda e persistida no DynamoDB. Neste trabalho, o grupo demonstra o fluxo por meio da arquitetura, do código e de valores esperados, pois não possui acesso aos recursos AWS.
