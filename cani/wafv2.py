"""Implement a v2 WAF"""

from constructs import Construct
from aws_cdk import (
    aws_wafv2 as waf,
)


class WAFv2(Construct):
    """Implement a v2 WAF"""

    def __init__(
        self, scope: Construct, construct_id: str, default_action="allow", **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.web_acl = waf.CfnWebACL(
            self,
            "WAF ACL",
            default_action={default_action: {}},
            scope="CLOUDFRONT",
            visibility_config={
                "sampledRequestsEnabled": True,
                "cloudWatchMetricsEnabled": True,
                "metricName": "web-acl",
            },
            rules=[
                {
                    "name": "Custom-RateLimit500",
                    "priority": 0,
                    "action": {"block": {}},
                    "visibilityConfig": {
                        "sampledRequestsEnabled": True,
                        "cloudWatchMetricsEnabled": True,
                        "metricName": "Custom-RateLimit500",
                    },
                    "statement": {
                        "rateBasedStatement": {"limit": 500, "aggregateKeyType": "IP"}
                    },
                },
                {
                    "priority": 1,
                    "overrideAction": {"none": {}},
                    "visibilityConfig": {
                        "sampledRequestsEnabled": True,
                        "cloudWatchMetricsEnabled": True,
                        "metricName": "AWS-AWSManagedRulesAmazonIpReputationList",
                    },
                    "name": "AWS-AWSManagedRulesAmazonIpReputationList",
                    "statement": {
                        "managedRuleGroupStatement": {
                            "vendorName": "AWS",
                            "name": "AWSManagedRulesAmazonIpReputationList",
                        },
                    },
                },
                {
                    "priority": 2,
                    "overrideAction": {"none": {}},
                    "visibilityConfig": {
                        "sampledRequestsEnabled": True,
                        "cloudWatchMetricsEnabled": True,
                        "metricName": "AWS-AWSManagedRulesCommonRuleSet",
                    },
                    "name": "AWS-AWSManagedRulesCommonRuleSet",
                    "statement": {
                        "managedRuleGroupStatement": {
                            "vendorName": "AWS",
                            "name": "AWSManagedRulesCommonRuleSet",
                        },
                    },
                },
                {
                    "priority": 3,
                    "overrideAction": {"none": {}},
                    "visibilityConfig": {
                        "sampledRequestsEnabled": True,
                        "cloudWatchMetricsEnabled": True,
                        "metricName": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
                    },
                    "name": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
                    "statement": {
                        "managedRuleGroupStatement": {
                            "vendorName": "AWS",
                            "name": "AWSManagedRulesKnownBadInputsRuleSet",
                        },
                    },
                },
                {
                    "priority": 4,
                    "overrideAction": {"none": {}},
                    "visibilityConfig": {
                        "sampledRequestsEnabled": True,
                        "cloudWatchMetricsEnabled": True,
                        "metricName": "AWS-AWSManagedRulesSQLiRuleSet",
                    },
                    "name": "AWS-AWSManagedRulesSQLiRuleSet",
                    "statement": {
                        "managedRuleGroupStatement": {
                            "vendorName": "AWS",
                            "name": "AWSManagedRulesSQLiRuleSet",
                        },
                    },
                },
            ],
        )

    @property
    def web_acl_arn(self):
        """return the arn of the acl"""
        return self.web_acl.attr_arn
