#!/usr/bin/env python3
"""all the apps for this stack"""
import os

import aws_cdk as cdk

from cani.cani_stack import CaniStack
from cani.cani_deployment import CaniPipelineStack
from cani.waf_stack import WafStack


app = cdk.App()
cani_stack = CaniStack(
    app,
    "CaniStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

CaniPipelineStack(
    app,
    "CaniPipelineStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)

waf_stack = WafStack(
    app,
    "WafStack",
    env=cdk.Environment(region="us-east-1", account=os.getenv("CDK_DEFAULT_ACCOUNT")),
)
cani_stack.add_dependency(waf_stack)


app.synth()
