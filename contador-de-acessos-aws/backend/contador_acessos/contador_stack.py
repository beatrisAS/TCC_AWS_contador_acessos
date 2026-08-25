from aws_cdk import (  # pyright: ignore[reportMissingImports]
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    RemovalPolicy,
)
from constructs import Construct  # pyright: ignore[reportMissingImports]

class ContadorAcessosStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

     
        tabela_contador = dynamodb.Table(
            self, "TabelaContador",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

      
        funcao_contador = _lambda.Function(
            self, "FuncaoContador",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="contador_lambda.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"NOME_TABELA": tabela_contador.table_name}
        )

   
        tabela_contador.grant_read_write_data(funcao_contador)


    
        api = apigw.LambdaRestApi(
            self, "ContadorApi",
            handler=funcao_contador,
            proxy=False,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            )
        )

        recurso_acessos = api.root.add_resource("acessos")
        recurso_acessos.add_method("GET")
