"""Retrieve a paramater"""
from datetime import datetime, timezone
from aws_cdk.custom_resources import (
        AwsCustomResource,
        AwsSdkCall,
        AwsCustomResourcePolicy,
        PhysicalResourceId)
from constructs import Construct

class SSMParameterReader(AwsCustomResource):
    """Obtain an SSM Paratmer"""
    def __init__(self, scope: Construct,
            construct_id: str,
            parameter_name: str,
            region: str,
            **kwargs
        ):

        self.parameter_name = parameter_name
        self.region = region

        dt_now = datetime.now()
        dt_now = dt_now.replace(tzinfo=timezone.utc)

        ssm_param = AwsSdkCall(
            service='SSM',
            action='getParameter',
            parameters={'Name': self.parameter_name},
            region=self.region,
            physical_resource_id=PhysicalResourceId.of(self.parameter_name+'-'+self.region+'v1')
                )

        super().__init__(scope, construct_id,
            on_update=ssm_param,
            policy=AwsCustomResourcePolicy.from_sdk_calls(
                resources=AwsCustomResourcePolicy.ANY_RESOURCE
                ),
             **kwargs
        )

    @property
    def parametervalue(self):
        """Return the response"""
        return str(self.get_response_field('Parameter.Value'))
