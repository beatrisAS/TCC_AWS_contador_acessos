from aws_cdk import (
    CfnOutput,
    Duration,
    RemovalPolicy,
    Stack,
    aws_apigateway as apigw,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_wafv2 as wafv2,
)
from constructs import Construct


class ClickOpsStack(Stack):
    """Infraestrutura conceitual do contador de acessos."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hits_table = dynamodb.Table(
            self,
            "ClickOpsHitsTable",
            table_name="AccessCounter",
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        counter_lambda = lambda_.Function(
            self,
            "ClickOpsCounterLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="contador.handler",
            code=lambda_.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
            environment={"TABLE_NAME": hits_table.table_name},
        )
        hits_table.grant_read_write_data(counter_lambda)

        api = apigw.RestApi(
            self,
            "ClickOpsApi",
            rest_api_name="ClickOps Contador Service",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=["POST", "OPTIONS"],
            ),
        )
        api.root.add_method("POST", apigw.LambdaIntegration(counter_lambda))

        frontend_bucket = s3.Bucket(
            self,
            "ClickOpsFrontendBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        web_acl = wafv2.CfnWebACL(
            self,
            "ClickOpsWebAcl",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="CLOUDFRONT",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="ClickOpsWafMetrics",
                sampled_requests_enabled=True,
            ),
            rules=[],
        )

        distribution = cloudfront.Distribution(
            self,
            "ClickOpsDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(frontend_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            web_acl_id=web_acl.attr_arn,
        )

        CfnOutput(
            self,
            "ApiGatewayUrl",
            value=api.url,
            description="URL conceitual da API do contador",
        )
        CfnOutput(
            self,
            "CloudFrontUrl",
            value=f"https://{distribution.distribution_domain_name}",
            description="URL conceitual da página",
        )
