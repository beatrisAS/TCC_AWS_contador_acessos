import json
import os
import boto3  # pyright: ignore[reportMissingImports]

NOME_TABELA = os.environ.get('NOME_TABELA', 'AccessCounter')
AWS_ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL')

def _tabela():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-east-1'),
        endpoint_url=AWS_ENDPOINT_URL or None,
    )
    return dynamodb.Table(NOME_TABELA)

def handler(event, context):
    try:
        response = _tabela().update_item(
            Key={'id': 'hits'},
            UpdateExpression='ADD acessos :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        novo_total = int(response['Attributes']['acessos'])
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({'mensagem': 'Sucesso', 'total_acessos': novo_total})
        }
    except Exception as e:
        print(f"Erro ao atualizar o DynamoDB: {e}")
        return {'statusCode': 500, 'body': json.dumps({'mensagem': 'Erro interno'})}
