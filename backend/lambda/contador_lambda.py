import json
import os

import boto3


def handler(event, context):
    """Incrementa o contador global em um item do DynamoDB."""
    table = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1")).Table(
        os.environ["TABLE_NAME"]
    )
    result = table.update_item(
        Key={"id": "hits"},
        UpdateExpression="ADD acessos :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )
    total = int(result["Attributes"]["acessos"])
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"id": "hits", "total_acessos": total}),
    }
