"""Create a WAF in us-east-1 for use by CloudFront"""
from constructs import Construct
from aws_cdk import Stack, aws_ssm as ssm
from .wafv2 import WAFv2


class WafStack(Stack):
    """Create a WAF in us-east-1 for use by CloudFront"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        waf_acl = WAFv2(self, "waf_acl")

        ssm.StringParameter(
            self,
            "waf_acl_arn",
            parameter_name="waf_acl_arn",
            description="WAF ACL ARN",
            string_value=waf_acl.web_acl_arn,
        )
