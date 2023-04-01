"""Can I pipeline"""
from aws_cdk import (
    Stack,
    Environment,
    Stage,
    pipelines,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit
)
from constructs import Construct

from .cani_stack import CaniStack

#
# Stack to hold the pipeline
#
class CaniPipelineStack(Stack):
    """The pipeline to deploy this thing"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defaults for all CodeBuild projects
        code_build_defaults = pipelines.CodeBuildOptions(  # pylint: disable=unused-variable
            # Control the build environment
            build_environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxArmBuildImage.AMAZON_LINUX_2_STANDARD_2_0,
                compute_type=codebuild.ComputeType.LARGE,
                privileged=True,
            ),
            partial_build_spec=codebuild.BuildSpec.from_object(
                {"phases": {"install": {"commands": ["n 14.19.0"]}}}
            ),
        )

        repository = codecommit.Repository.from_repository_name(self, "cani_repo", repository_name="cani")

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            code_build_defaults=code_build_defaults,
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(
                    repository = repository,
                    branch = 'main'
                ),
                install_commands=["n 14.19.0"],
                commands=[
                    "pip install -r requirements.txt",
                    "npm install -g aws-cdk",
                    "cdk synth",
                ],
            ),
        )

        pipeline.add_stage(
            CaniStage(
                self,
                "CaniStack",
                env=Environment(account="025705368789", region="ap-southeast-2"),
            )
        )


class CaniStage(Stage):
    """Deploy the app"""

    def __init__(self, scope, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        CaniStack(self, "caniStack", stack_name="CaniStack")
