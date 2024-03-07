import hashlib
import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

import boto3
from attr import Factory, define, field

from hangar_sdk.core import ExecutionType, IResource
from hangar_sdk.core.terraform import Resource, ResourceGroup
from hangar_sdk.resources.terraform.aws import (
    aws_alb,
    aws_ebs_volume,
    aws_instance,
    aws_internet_gateway,
    aws_lambda_function,
    aws_lambda_layer_version,
    aws_lb_listener,
    aws_lb_target_group,
    aws_s3_bucket,
    aws_security_group,
    aws_subnet,
    aws_vpc,
    data_aws_ami,
    data_aws_vpc,
)

# Bucket

# The Done Line ----------------

# VPC
# Subnet
# Volume
# IGW
# Loadbalancer (LB, Target group, Listener, need listener rules)
# Security Group

# Code Written -----------------

# ECS

# Lift and shift

# Instance
# Autoscale
# Lambda

# Docker compose to task defn
# Fargate


def hash_path(path):
    """Return a hash for the specified file or directory."""
    hasher = hashlib.sha1()
    if os.path.isfile(path):
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                filepath = os.path.join(root, name)
                hasher.update(hash_path(filepath).encode())
    return hasher.hexdigest()


@define(kw_only=True, slots=False)
class AwsL1Resource(Resource, ABC):
    name: str
    group: "ResourceGroup"
    _dependencies: list = field(default=Factory(list))
    tags: Optional[dict] = None

    @abstractmethod
    def _resolve(self, type: ExecutionType = "create") -> Sequence[IResource]:
        pass

    @abstractmethod
    def get_client(self) -> Any:
        pass


@define(kw_only=True, slots=False)
class AwsIamRole(Resource):
    name: str
    group: "ResourceGroup"
    _dependencies: list = field(default=Factory(list))

    def resolve(self):
        return


@define(kw_only=True, slots=False)
class AwsBucket(Resource):
    name: str
    group: "ResourceGroup"
    _dependencies: list = field(default=Factory(list))
    tags: Optional[dict] = None

    def _resolve(self, type: ExecutionType = "create"):
        self.bucket = aws_s3_bucket.AwsS3Bucket(
            group=self.group,
            top_name=self.name,
            bucket=self.name,
            tags=self.tags,
            force_destroy=True,
        )

        return [self.bucket]

    def get_client(self):
        return boto3.client("s3")

    def put_object(self, key: str, source: str):
        print(f"Uploading Object to bucket {self.name}")

        client = self.get_client()
        client.upload_file(source, self.name, key)

        print(f"Finished Uploading Object to bucket {self.name}")


@define(kw_only=True, slots=False)
class DefaultAwsVpc(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    tags: dict

    def _resolve(self, type: ExecutionType = "create"):
        self.vpc = data_aws_vpc.DataAwsVpc(
            top_name=self.name,
            group=self.group,
            default=True,
        )

        return [self.vpc]


@define(kw_only=True, slots=False)
class AwsVpc(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    cidr_block: str
    tags: dict

    def _resolve(self, type: ExecutionType = "create"):
        self.vpc = aws_vpc.AwsVpc(
            group=self.group,
            top_name=self.name,
            cidr_block=self.cidr_block,
            tags=self.tags,
        )

        return [self.vpc]


@define(kw_only=True, slots=False)
class AwsSubnet(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    vpc: Union[AwsVpc, DefaultAwsVpc]
    cidr_block: Optional[str] = None
    availability_zone: str
    tags: dict
    public: bool = True

    def _resolve(self, type: ExecutionType = "create"):
        self.subnet = aws_subnet.AwsSubnet(
            group=self.group,
            top_name=self.name,
            cidr_block=self.cidr_block if self.cidr_block else "0.0.0.0/0",
            availability_zone=self.availability_zone,
            tags=self.tags,
            map_public_ip_on_launch=self.public,
            vpc_id=self.vpc.vpc.ref().id,
        )

        return [self.subnet]


@define(kw_only=True, slots=False)
class AwsVolume(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    availability_zone: str
    size: int
    tags: dict

    def _resolve(self, type: ExecutionType = "create"):
        self.volume = aws_ebs_volume.AwsEbsVolume(
            group=self.group,
            top_name=self.name,
            availability_zone=self.availability_zone,
            size=self.size,
            tags=self.tags,
        )

        return [self.volume]


@define(kw_only=True, slots=False)
class AwsInternetGateway(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    tags: Optional[Dict[str, str]] = None
    tags_all: Union[Dict[str, str], None] = None
    vpc: AwsVpc

    def _resolve(self, type: ExecutionType = "create") -> List[IResource]:
        self.ig = aws_internet_gateway.AwsInternetGateway(
            top_name=self.name,
            group=self.group,
            tags=self.tags,
            tags_all=self.tags_all,
            vpc_id=self.vpc.vpc.ref().id,
        )

        return [self.ig]


@define(kw_only=True, slots=False)
class Ingress:
    to_port: int
    from_port: int
    protocol: str
    cidr_blocks: Optional[List[str]] = None


@define(kw_only=True, slots=False)
class Egress:
    to_port: int
    from_port: int
    protocol: str
    cidr_blocks: Optional[List[str]] = None


@define(kw_only=True, slots=False)
class AwsSecurityGroup(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    egress: Optional[List[Egress]] = None
    ingress: Optional[List[Ingress]] = None

    def _resolve(self, type: ExecutionType = "create") -> List[IResource]:
        self.security_group = aws_security_group.AwsSecurityGroup(
            top_name=self.name,
            group=self.group,
            description=None,
            egress=[
                aws_security_group.Egress(
                    group=self.group,
                    from_port=egress.from_port,
                    to_port=egress.to_port,
                    protocol=egress.protocol,
                    cidr_blocks=egress.cidr_blocks,
                )
                for egress in self.egress
            ]
            if self.egress
            else None,
            ingress=None,
            name=None,
            name_prefix=None,
            revoke_rules_on_delete=None,
            tags=None,
            tags_all=None,
            timeouts=None,
            vpc_id=None,
        )

        return [self.security_group]


@define(kw_only=True, slots=False)
class AwsLoadBalancer(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    tags: Optional[Dict[str, str]] = None
    internal: bool = False
    securityGroups: List[AwsSecurityGroup]
    subnets: List[AwsSubnet]

    def _resolve(self, type: ExecutionType = "create") -> Sequence[IResource]:
        self.lb = aws_alb.AwsAlb(
            top_name=self.name,
            group=self.group,
            internal=self.internal,
            security_groups=[sg.security_group.ref().id for sg in self.securityGroups]
            if self.securityGroups
            else None,
            subnets=[subnet.subnet.ref().id for subnet in self.subnets]
            if self.subnets
            else None,
            tags=self.tags,
        )

        return [self.lb]


@define(kw_only=True, slots=False)
class AwsLbTargetGroup(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    port: int
    protocol: str
    healthcheck_path: str
    vpc_id: str

    def _resolve(self, type: ExecutionType = "create") -> List[IResource]:
        self.target_group = aws_lb_target_group.AwsLbTargetGroup(
            group=self.group,
            top_name=self.name,
            name=self.name,
            port=self.port,
            protocol=self.protocol,
            vpc_id=self.vpc_id,
            health_check=[
                aws_lb_target_group.HealthCheck(
                    group=self.group, path=self.healthcheck_path
                )
            ],
        )

        return [self.target_group]


@define(kw_only=True, slots=False)
class AwsLbListener(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    load_balancer: AwsLoadBalancer
    port: int
    protocol: str
    target_group: AwsLbTargetGroup

    def _resolve(self, type: ExecutionType = "create") -> List[IResource]:
        self.aws_lb_listener = aws_lb_listener.AwsLbListener(
            top_name=self.name,
            group=self.group,
            load_balancer_arn=self.load_balancer.lb.ref().arn,
            port=self.port,
            protocol=self.protocol,
            default_action=[
                aws_lb_listener.DefaultAction(
                    group=self.group,
                    type="forward",
                    target_group_arn=self.target_group.target_group.ref().arn,
                )
            ],
        )

        return [self.aws_lb_listener]


@define(kw_only=True, slots=False)
class AwsEC2Instance(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    ami: str
    instance_type: str
    architecture: Union[Literal["x86_64"], Literal["arm64"]]
    subnet: AwsSubnet
    tags: dict
    os: str = "ubuntu"

    def _resolve(self, type: ExecutionType = "create"):
        self.ubuntu2204 = data_aws_ami.DataAwsAmi(
            top_name=self.name + "-ami",
            group=self.group,
            most_recent=True,
            owners=["099720109477"],
            filter=[
                data_aws_ami.Filter(
                    group=self.group,
                    name="architecture",
                    values=[self.architecture],
                ),
                data_aws_ami.Filter(
                    group=self.group,
                    name="virtualization-type",
                    values=["hvm"],
                ),
                data_aws_ami.Filter(
                    group=self.group,
                    name="name",
                    values=[
                        "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-*"
                        if self.architecture == "x86_64"
                        else "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-arm64-*"
                    ],
                ),
            ],
        )

        self.instance = aws_instance.AwsInstance(
            group=self.group,
            top_name=self.name,
            ami=self.ubuntu2204.ref().id,
            instance_type=self.instance_type,
            subnet_id=self.subnet.subnet.ref().id,
            tags=self.tags,
        )

        return [self.ubuntu2204, self.instance]

    def get_instance_client(self):
        return boto3.resource("ec2")

    def run_commands(self, commands: List[str]):
        pass


@define(kw_only=True, slots=False)
class ArchiveAsset(Resource):
    name: str
    group: ResourceGroup
    _dependencies: list = field(default=Factory(list))
    path: str
    bucket: AwsBucket

    @property
    def computed_path(self):
        return os.path.basename(self.path) + "-" + hash_path(self.path)

    def _resolve(self, type: ExecutionType = "create"):
        if type == "create":
            print(f"Syncing asset archive {self.name}")

            self.bucket.put_object(
                key=self.computed_path,
                source=self.path,
            )

            print(f"Finished syncing asset archive {self.name}")

        return []


@define(kw_only=True, slots=False)
class LambdaLayer(AwsL1Resource):
    asset: ArchiveAsset
    group: ResourceGroup
    runtimes: Union[List[str], None] = None

    def _resolve(self, type: ExecutionType = "create"):
        self.layer = aws_lambda_layer_version.AwsLambdaLayerVersion(
            group=self.group,
            top_name=self.name,
            s3_bucket=self.asset.bucket.bucket.ref().id,
            s3_key=os.path.basename(self.asset.computed_path),
            compatible_runtimes=self.runtimes,
            layer_name=self.name,
        )

        return [self.layer]

    def get_client(self):
        return boto3.client("lambda")


@define(kw_only=True, slots=False)
class LambdaFunction(AwsL1Resource):
    name: str
    function_name: str
    group: ResourceGroup
    asset: ArchiveAsset
    runtime: str
    handler: str
    role: str
    timeout: Optional[int] = None
    environment: Union[Dict[str, str], None] = None
    layers: Union[List[LambdaLayer], None] = None

    def _resolve(self, type: ExecutionType = "create"):
        # print(self._dependencies)

        self.function = aws_lambda_function.AwsLambdaFunction(
            group=self.group,
            top_name=self.name,
            function_name=self.function_name,
            s3_bucket=self.asset.bucket.bucket.ref().id,
            s3_key=os.path.basename(self.asset.computed_path),
            runtime=self.runtime,
            handler=self.handler,
            timeout=self.timeout,
            role=self.role,
            environment=[
                aws_lambda_function.Environment(
                    group=self.group, variables=self.environment
                )
            ],
            layers=[layer.layer.ref().arn for layer in self.layers]
            if self.layers
            else None,
        )

        return [self.function]

    def get_client(self):
        return boto3.client("lambda")

    def invoke(self, payload: dict):
        client = self.get_client()
        response = client.invoke(
            FunctionName=self.state["aws_lambda_function"][self.name]["values"][
                "function_name"
            ],
            Payload=json.dumps(payload),
        )
        return json.loads(response["Payload"].read().decode("utf-8"))
