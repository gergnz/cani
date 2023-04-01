"""Can I module"""
from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    Fn,
    # aws_sqs as sqs,
)
from constructs import Construct


class CaniStack(Stack):
    """Can I stack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cani_vpc = ec2.Vpc(self, "cani_vpc", nat_gateways=0)

        ip6_cidr = ec2.CfnVPCCidrBlock(
            self,
            "cidr_v6",
            vpc_id=cani_vpc.vpc_id,
            amazon_provided_ipv6_cidr_block=True,
        )

        all_subnets = []

        all_subnets = (
            cani_vpc.public_subnets
            + cani_vpc.private_subnets
            + cani_vpc.isolated_subnets
        )

        vpc_v6_cidr = Fn.select(0, cani_vpc.vpc_ipv6_cidr_blocks)
        subnet_v6_cidrs = Fn.cidr(vpc_v6_cidr, 256, str(128 - 64))

        for i, subnet in enumerate(all_subnets):
            cidr6 = Fn.select(i, subnet_v6_cidrs)
            sub_node = subnet.node.default_child
            sub_node.ipv6_cidr_block = cidr6
            subnet.node.add_dependency(ip6_cidr)

        if cani_vpc.public_subnets:
            igw_id = cani_vpc.internet_gateway_id

            for subnet in cani_vpc.public_subnets:
                subnet.add_route(
                    "DefaultRoute6",
                    router_type=ec2.RouterType.GATEWAY,
                    router_id=igw_id,
                    destination_ipv6_cidr_block="::/0",
                    enables_internet_connectivity=True,
                )
        if cani_vpc.private_subnets:
            eigw = ec2.CfnEgressOnlyInternetGateway(
                self, "eigw6", vpc_id=cani_vpc.vpc_id
            )

            for subnet in cani_vpc.private_subnets:
                subnet.add_route(
                    "DefaultRoute6",
                    router_type=ec2.RouterType.EGRESS_ONLY_INTERNET_GATEWAY,
                    router_id=eigw,
                    destination_ipv6_cidr_block="::/0",
                    enables_internet_connectivity=True,
                )
