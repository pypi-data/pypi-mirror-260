import os
import boto3
from botocore.config import Config
from botocore import client

if "FINTEKKERS_CLUSTER_NAME" not in os.environ:
    print("Missing environment variable: FINTEKKERS_CLUSTER_NAME")

if "AWS_ACCESS_KEY_ID" not in os.environ:
    print("Missing environment variable: AWS_ACCESS_KEY_ID")

if "AWS_SECRET_ACCESS_KEY" not in os.environ:
    print("Missing environment variable: AWS_SECRET_ACCESS_KEY")

ORG_NAME = "fintekkers"
CLUSTER_NAME = (
    os.environ["FINTEKKERS_CLUSTER_NAME"]
    if "FINTEKKERS_CLUSTER_NAME" in os.environ
    else ORG_NAME.lower()
)
print("CLUSTER_NAME: {}".format(CLUSTER_NAME))

REGION_NAME = (
    os.environ["FINTEKKERS_REGION_NAME"]
    if "FINTEKKERS_REGION_NAME" in os.environ
    else "us-east-1"
)
print("REGION_NAME: {}".format(REGION_NAME))

VPC_NAME = "{}-vpc".format(ORG_NAME)
print("VPC_NAME: {}".format(VPC_NAME))

SERVICE_NAME = (
    os.environ["FINTEKKERS_SERVICE_NAME"]
    if "FINTEKKERS_SERVICE_NAME" in os.environ
    else "{}-dummy-service".format(CLUSTER_NAME)
)
print("SERVICE_NAME: {}".format(SERVICE_NAME))

REPOSITORY_NAME = (
    os.environ["FINTEKKERS_REPOSITORY_NAME"]
    if "FINTEKKERS_REPOSITORY_NAME" in os.environ
    else SERVICE_NAME
)
print("REPOSITORY_NAME: {}".format(REPOSITORY_NAME))

FAMLILY_NAME = (
    os.environ["FINTEKKERS_FAMLILY_NAME"]
    if "FINTEKKERS_FAMLILY_NAME" in os.environ
    else CLUSTER_NAME
)
print("FAMLILY_NAME: {}".format(FAMLILY_NAME))

TARGET_GROUP_NAME = (
    os.environ["FINTEKKERS_TARGET_GROUP_NAME"]
    if "FINTEKKERS_TARGET_GROUP_NAME" in os.environ
    else CLUSTER_NAME + "-target-group"[:30]
)

print("TARGET_GROUP_NAME: {}".format(TARGET_GROUP_NAME))

LOAD_BALANCER_NAME = (
    os.environ["FINTEKKERS_LOAD_BALANCER_NAME"]
    if "FINTEKKERS_LOAD_BALANCER_NAME" in os.environ
    else CLUSTER_NAME + "-lb"
)
print("LOAD_BALANCER_NAME: {}".format(LOAD_BALANCER_NAME))

IMAGE_URL = "754996918532.dkr.ecr.us-east-1.amazonaws.com/{}".format(SERVICE_NAME)
print("IMAGE_URL: {}".format(IMAGE_URL))


def get_config():
    return Config(
        region_name=REGION_NAME,
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )


def get_ecs_client() -> client:
    return boto3.client("ecs", config=get_config())


def get_acm_client() -> client:
    return boto3.client("acm", config=get_config())


def get_ecr_client() -> client:
    return boto3.client("ecr", config=get_config())


def get_ec2_client() -> client:
    return boto3.client("ec2", config=get_config())


def get_elb_client() -> client:
    return boto3.client("elbv2", config=get_config())


def is_any_clusters(ecs_session) -> bool:
    ecs_clusters = ecs_session.list_clusters()

    if len(ecs_clusters["clusterArns"]) > 0:
        cluster_arn = ecs_clusters["clusterArns"][0]
        print("There is already an ECS cluster: {}. Halting".format(cluster_arn))

        cluster_info = ecs_session.describe_clusters(clusters=[cluster_arn])
        print(cluster_info)
        return True

    return False


def get_cluster_arn(ecs_session) -> str:
    ecs_clusters = ecs_session.list_clusters()

    if len(ecs_clusters["clusterArns"]) == 1:
        return ecs_clusters["clusterArns"][0]
    else:
        raise ValueError(
            "Expecting only 1 cluster but there were {}".format(
                len(ecs_clusters["clusterArns"])
            )
        )


def get_security_group_id(optional_group_name="") -> str:
    security_groups = get_ec2_client().describe_security_groups()["SecurityGroups"]

    sg_name = (
        optional_group_name
        if len(optional_group_name) > 0
        else "fintekkers-security-group"
    )
    fintekkers_groups = list(
        filter(lambda sg: sg_name in sg["GroupName"], security_groups)
    )

    if len(fintekkers_groups) == 0:
        raise ValueError("There are no security groups for {}".format(sg_name))
    elif len(fintekkers_groups) == 1:
        return fintekkers_groups[0]["GroupId"]
    else:
        raise ValueError(
            "More security groups than expected. Expected 1, got {}".format(
                len(fintekkers_groups)
            )
        )


def get_public_subets():
    # TODO - Check there are 2 public subnets in 2 AZs. If not, create them!
    ec2_client = get_ec2_client()

    subnets = ec2_client.describe_subnets()

    def filter_publc(subnet):
        if "Tags" in subnet:
            tags = subnet["Tags"]
            for tag in tags:
                if tag["Key"] == "Name" and "public" in tag["Value"]:
                    return True

        return False

    public_subnets = list(filter(filter_publc, subnets["Subnets"]))

    if len(public_subnets) < 2:
        raise ValueError("There should be 2 subnets that are public, only found 1")

    return public_subnets


def get_public_subets_arns() -> list:
    subnets = get_public_subets()

    subnet_arns = []

    for subnet in subnets:
        subnet_arns.append(subnet["SubnetId"])

    return subnet_arns


def create_vpc():
    if True:
        raise ValueError("Create through the VPC wizard (and more) in the AWS console")

    vpc = get_ec2_client().create_vpc(
        CidrBlock="10.0.0.0/24",
        AmazonProvidedIpv6CidrBlock=False,
        # Ipv6Pool='string',
        # Ipv6CidrBlock='string',
        # Ipv4IpamPoolId='string',
        # Ipv4NetmaskLength=123,
        # Ipv6IpamPoolId='string',
        # Ipv6NetmaskLength=123,
        DryRun=False,
        InstanceTenancy="default",  # |'dedicated'|'host',
        # Ipv6CidrBlockNetworkBorderGroup='string',
        TagSpecifications=[
            {"ResourceType": "vpc", "Tags": [{"Key": "Name", "Value": VPC_NAME}]},
        ],
    )
    return vpc


def get_vpc_id():
    vpcs = get_ec2_client().describe_vpcs()

    for vpc in vpcs["Vpcs"]:
        if "Tags" in vpc:
            for tag in vpc["Tags"]:
                if tag["Key"] == "Name" and VPC_NAME in tag["Value"]:
                    return vpc["VpcId"]

    raise ValueError("No VPC found called {}".format(VPC_NAME))


def get_target_group_arn(port: str = None) -> str:
    elb_client = get_elb_client()

    target_groups = elb_client.describe_target_groups()["TargetGroups"]
    # Kind of equivalent to the below.

    # aws elbv2 create-target-group --name $SERVICE_FAMILY_NAMEtargetgroup
    # --protocol HTTP --port 81 --health-check-protocol HTTP --health-check-port 81
    # --health-check-path /health --health-check-interval-seconds 1 --health-check-timeout-seconds 4
    # --target-type ip --tags Key=string,Value=string --vpc-id $TMP_VPC_ID
    # export TMP_VPC_ID=$(aws ec2 describe-vpcs --filter Name=tag:Name,Values=group0 | jq '.Vpcs[0].VpcId' -r)

    if len(target_groups) == 0:
        return None  # No target groups
    elif len(target_groups) > 0:
        for target_group in target_groups:
            if int(target_group["Port"]) == port:
                return target_group["TargetGroupArn"]

        return None  # No target group with this port
    else:
        raise ValueError("There are multiple target groups, which isn't expected")


def get_load_balancer(load_balancer_arn: str):
    response = get_elb_client().describe_load_balancers(
        LoadBalancerArns=[load_balancer_arn],
        # Names=[
        #     LOAD_BALANCER_NAME
        # ],
        # Marker='string',
        # PageSize=123
    )

    if len(response["LoadBalancers"]) == 0:
        raise ValueError("No load balancer found with arn {}".format(load_balancer_arn))

    return response["LoadBalancers"][0]


def get_load_balancer_arn():
    try:
        response = get_elb_client().describe_load_balancers(
            # LoadBalancerArns=[
            # ],
            Names=[LOAD_BALANCER_NAME],
            # Marker='string',
            # PageSize=123
        )

        if "LoadBalancers" in response and len(response["LoadBalancers"]) > 0:
            # list(map(lambda x: x['LoadBalancerName'], response['LoadBalancers']))
            lbs = list(
                filter(
                    lambda x: LOAD_BALANCER_NAME in x["LoadBalancerName"],
                    response["LoadBalancers"],
                )
            )
            if len(lbs) == 1:
                load_balancer_arn = lbs[0]["LoadBalancerArn"]
                print(
                    "Load balancer already created with name {}. {}".format(
                        LOAD_BALANCER_NAME, load_balancer_arn
                    )
                )
                return load_balancer_arn
            else:
                raise ValueError(
                    "There are multiple load balancers with name {}".format(
                        LOAD_BALANCER_NAME
                    )
                )
    except:
        print("There is no load balancer with name {}".format(LOAD_BALANCER_NAME))

    return None


def get_listener_arn(load_balancer_arn: str, port: str = None):
    if load_balancer_arn is None:
        print("There is no listener, as there is no load balancer set up")
        return None

    response = get_elb_client().describe_listeners(
        LoadBalancerArn=load_balancer_arn,
        # ListenerArns=[
        #     'string',
        # ],
        # Marker='string',
        # PageSize=123
    )

    # If default port is empty and there is only one listener, return it

    if port is None and len(response["Listeners"]) == 1:
        listener_arn = response["Listeners"][0]["ListenerArn"]
        print(
            "Listener {} is already attached to load balancer {}".format(
                listener_arn, load_balancer_arn
            )
        )
        return listener_arn
    # If default port is not empty, only return the listener if it exists for that port

    elif len(response["Listeners"]) > 0:
        for listener in response["Listeners"]:
            if listener["Port"] == int(port):
                listener_arn = listener["ListenerArn"]
                print(
                    "Listener {} is already attached to load balancer {}".format(
                        listener_arn, load_balancer_arn
                    )
                )
                return listener_arn
    else:
        return None


def get_container_registry_arn(service_repository_name: str) -> str:
    ecr_session = get_ecr_client()

    response = ecr_session.describe_repositories()
    repositories = response["repositories"]

    if len(repositories) == 0:
        raise ValueError("No repositories found")

    for repository in repositories:
        if service_repository_name == repository["repositoryName"]:
            return repository["repositoryArn"]

    raise ValueError(
        "Could not find repository with name {}".format(service_repository_name)
    )


def setup_cluster():
    ecs_session = get_ecs_client()

    if not is_any_clusters(ecs_session):
        print("Creating cluster")
        result = ecs_session.create_cluster(clusterName=CLUSTER_NAME)
        print("Response from AWS: {}".format(result))


if __name__ == "__main__":
    setup_cluster()
