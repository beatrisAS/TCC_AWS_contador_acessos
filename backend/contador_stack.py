from aws_cdk import (  # type: ignore[import-not-found]
    CfnOutput,
    Duration,
    Stack,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
)
from constructs import Construct


class ContadorAcessosStack(Stack):
    """Infraestrutura planejada para a versão AWS do contador."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(
            self,
            "ContadorTable",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        function = lambda_.Function(
            self,
            "ContadorFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="contador_lambda.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
            environment={"TABLE_NAME": table.table_name},
        )
        table.grant_read_write_data(function)

        api = apigw.LambdaRestApi(self, "ContadorApi", handler=function, proxy=False)
        api.root.add_resource("acessos").add_method("GET")

        CfnOutput(self, "ApiUrl", value=api.url_for_path("acessos"))
        CfnOutput(self, "TableName", value=table.table_name)
