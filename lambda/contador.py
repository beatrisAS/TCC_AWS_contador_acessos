import json
import os

import boto3


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def handler(event, context):
    """Registra um acesso e retorna o total atualizado."""
    table_name = os.environ.get("TABLE_NAME")
    if not table_name:
        return _response(500, {"error": "TABLE_NAME não configurada"})

    try:
        table = boto3.resource("dynamodb").Table(table_name)
        result = table.update_item(
            Key={"id": "hits"},
            UpdateExpression="ADD total :increment",
            ExpressionAttributeValues={":increment": 1},
            ReturnValues="UPDATED_NEW",
        )
        total = int(result["Attributes"]["total"])
        return _response(200, {"message": "Acesso registrado", "total": total})
    except Exception as error:
        print(f"Erro ao atualizar o contador: {error}")
        return _response(500, {"error": "Não foi possível atualizar o contador"})
