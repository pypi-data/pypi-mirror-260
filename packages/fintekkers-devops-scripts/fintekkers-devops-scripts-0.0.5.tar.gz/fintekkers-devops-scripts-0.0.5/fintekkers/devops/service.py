import ast
from fintekkers.devops.aws_account_setup import *

# SERVICE_AND_TASK_NAME = get_image_tag_name()
DEFAULT_PORT = (
    5001
    if "FINTEKKERS_DEFAULT_PORT" not in os.environ
    else int(os.environ["FINTEKKERS_DEFAULT_PORT"])
)
print("DEFAULT_PORT: {}".format(DEFAULT_PORT))

TASK_COUNT = 1
print("TASK_COUNT: {}".format(TASK_COUNT))

PROTOCOL = (
    "HTTP"
    if "FINTEKKERS_PROTOCOL" not in os.environ
    else os.environ["FINTEKKERS_PROTOCOL"]
)
print("PROTOCOL: {}".format(PROTOCOL))

IS_GPRC = (
    False
    if "FINTEKKERS_IS_GRPC" not in os.environ
    else ast.literal_eval(os.environ["FINTEKKERS_IS_GRPC"])
)
print("IS_GPRC: {}".format(IS_GPRC))

HEALTH_CHECK_PATH = (
    "/Health/Check"
    if "FINTEKKERS_HEALTH_CHECK_PATH" not in os.environ
    else os.environ["FINTEKKERS_HEALTH_CHECK_PATH"]
)
print("HEALTH_CHECK_PATH: {}".format(HEALTH_CHECK_PATH))

TASK_CPU = (
    "512"
    if "FINTEKKERS_TASK_CPU" not in os.environ
    else str(ast.literal_eval(os.environ["FINTEKKERS_TASK_CPU"]))
)
print("TASK_CPU: {}".format(TASK_CPU))

TASK_MEMORY = (
    "1024"
    if "FINTEKKERS_TASK_MEMORY" not in os.environ
    else str(ast.literal_eval(os.environ["FINTEKKERS_TASK_MEMORY"]))
)
print("TASK_MEMORY: {}".format(TASK_MEMORY))


DOMAIN_NAME = "api.fintekkers.org"
KEY_PAIR_NAME = "fintekkers-test-ec2"


def create_task_definition():
    # Create a task definition
    # Fargate launch types have considerations. See https://docs.aws.amazon.com/AmazonECS/latest/userguide/fargate-task-defs.html
    response = get_ecs_client().register_task_definition(
        networkMode="awsvpc",
        containerDefinitions=[
            {
                # #Only required for images hosted outside of ECR that are private
                # # See https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
                # # And https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_ECS.html
                # "repositoryCredentials":{
                #         'credentialsParameter': 'string'
                #         #TODO
                #     },
                "name": SERVICE_NAME,
                "links": [],
                "image": IMAGE_URL,
                "essential": True,
                "portMappings": [
                    {"containerPort": DEFAULT_PORT, "hostPort": DEFAULT_PORT}
                ],
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": CLUSTER_NAME,
                        "awslogs-region": REGION_NAME,
                        "awslogs-create-group": "true",
                        "awslogs-stream-prefix": SERVICE_NAME,
                    },
                },
                # "healthCheck": {
                #     "startPeriod" : 60
                # }
                # By not specifying memory/CPU, docker will try to use all available memory
                # Not 100% sure if this should be reduced to allow for system overhead
                #   "memory": 256,
                #   "cpu": 10
            }
        ],
        family=SERVICE_NAME,
        requiresCompatibilities=[
            "FARGATE",
        ],
        cpu=TASK_CPU,
        memory=TASK_MEMORY,
        executionRoleArn="arn:aws:iam::754996918532:role/ecsTaskExecutionRole",
        taskRoleArn="arn:aws:iam::754996918532:role/ecsTaskExecutionRole",
    )

    print(
        "Revision {} created of {}".format(
            response["taskDefinition"]["revision"], FAMLILY_NAME
        )
    )
    return response["taskDefinition"]["taskDefinitionArn"]


def create_target_group():
    # aws elbv2 create-target-group --name $SERVICE_FAMILY_NAMEtargetgroup
    # --protocol HTTP --port 81 --health-check-protocol HTTP --health-check-port 81
    # --health-check-path /health --health-check-interval-seconds 1 --health-check-timeout-seconds 4
    # --target-type ip --tags Key=string,Value=string --vpc-id $TMP_VPC_ID
    # export TMP_VPC_ID=$(aws ec2 describe-vpcs --filter Name=tag:Name,Values=group0 | jq '.Vpcs[0].VpcId' -r)

    target_group_arn = get_target_group_arn(DEFAULT_PORT)
    if target_group_arn is not None:
        return target_group_arn
    else:
        vpc_id = get_vpc_id()
        protocol_version = "GRPC" if IS_GPRC else "HTTP1"
        healthcheck_protocol = "HTTP" if IS_GPRC else PROTOCOL
        healthcheck_path = HEALTH_CHECK_PATH
        print(
            "Creating target group called {} in VPC: {}".format(
                TARGET_GROUP_NAME, vpc_id
            )
        )

        print(
            "Target group will receive traffic via {} on port {}. The health check "
            "will be checked against the path {} via {} on port {}".format(
                protocol_version,
                DEFAULT_PORT,
                healthcheck_path,
                "HTTP",
                healthcheck_path,
            )
        )

        response = get_elb_client().create_target_group(
            Name=TARGET_GROUP_NAME,
            Protocol="HTTP",  # |'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
            ProtocolVersion=protocol_version,
            Port=DEFAULT_PORT,
            VpcId=vpc_id,
            HealthCheckProtocol=healthcheck_protocol,  # |'HTTPS'|'TCP'|'TLS'|'UDP'|'TCP_UDP'|'GENEVE',
            HealthCheckPort="{}".format(DEFAULT_PORT),
            HealthCheckEnabled=True,  # This must be true for IP based services (which fargate is)
            HealthCheckPath=healthcheck_path,
            HealthCheckIntervalSeconds=20,
            HealthCheckTimeoutSeconds=4,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=10,
            Matcher={
                # 'HttpCode': 'string',
                "GrpcCode": "0-99"
            },
            TargetType="ip",  # Fargate uses IP based services. Other values are non-fargate: |'lambda'|'alb'|'instance',
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            IpAddressType="ipv4",  # |'ipv6'
        )
        return response["TargetGroups"][0]["TargetGroupArn"]


def create_load_balancer() -> str:
    lb_arn = get_load_balancer_arn()
    if lb_arn is not None:
        return lb_arn
    else:
        print("Creating load balancer with name '{}'".format(LOAD_BALANCER_NAME))
        # aws elbv2 create-load-balancer --name davetestsimplehttploadbalancer3 --type application --subnets $TMP_SUBNET_0_ID $TMP_SUBNET_1_ID --security-groups=$TMP_SECURITY_GROUP --ip-address-type ipv4
        # defaults to internet facing and ip4
        response = get_elb_client().create_load_balancer(
            Name=LOAD_BALANCER_NAME,
            Subnets=get_public_subets_arns(),
            SecurityGroups=[get_security_group_id()],
            Scheme="internet-facing",  # |'internal',
            # Tags=[
            #     {
            #         'Key': 'string',
            #         'Value': 'string'
            #     },
            # ],
            Type="application",  # |'network'|'gateway',
            IpAddressType="ipv4",  # |'dualstack',
            # CustomerOwnedIpv4Pool='string'
        )

        return response["LoadBalancers"][0]["LoadBalancerArn"]


def get_cert_arn():
    certs = get_acm_client().list_certificates(CertificateStatuses=["ISSUED"])
    certs = certs["CertificateSummaryList"]
    if len(certs) == 1:
        return certs[0]["CertificateArn"]

    for cert in certs:
        domains = cert["SubjectAlternativeNameSummaries"]

        for domain in domain:
            if DOMAIN_NAME in domain:
                return cert["CertificateArn"]

    raise ValueError(
        "Could not find certificate for {}. There were {} certs".format(
            DOMAIN_NAME, len(certs)
        )
    )


def attach_load_balancer_and_target_group(
    target_group_arn: str, load_balancer_arn: str
):
    # ASSOCIATE THE LOAD BALANCER WITH THE TARGET GROUP
    listener_arn = get_listener_arn(load_balancer_arn, DEFAULT_PORT)

    if listener_arn is not None:
        return listener_arn

    response = get_elb_client().create_listener(
        DefaultActions=[
            {
                "TargetGroupArn": target_group_arn,
                "Type": "forward",
            },
        ],
        LoadBalancerArn=load_balancer_arn,
        Port=DEFAULT_PORT,
        Protocol=PROTOCOL,
        # SslPolicy='string',
        Certificates=[
            {
                "CertificateArn": get_cert_arn(),
                #         'IsDefault': True|False #You don't provide this when providing the arn
            },
        ],
    )

    return response["Listeners"][0]["ListenerArn"]


def await_load_balancer(load_balancer_arn):
    # Check can access load balancer
    lb = get_load_balancer(get_load_balancer_arn())
    url = lb["DNSName"]
    import time, requests as r

    sleep_time = 2
    tries = 60

    print(
        "Will call {} repeatedly for {}+ seconds to ensure service was up and running the whole time. Will only print errors".format(
            url, sleep_time * tries
        )
    )

    request_url = "{}://{}:{}".format(PROTOCOL, url, DEFAULT_PORT)

    for i in range(tries):
        time.sleep(sleep_time)

        lb = get_load_balancer(get_load_balancer_arn())
        if lb["State"]["Code"] != "active":
            print(
                "Load balancer is not in an active state yet ({})".format(
                    lb["State"]["Code"]
                )
            )
            break

        try:
            response = r.get(request_url, verify=False)
            if response.status_code == 464:
                print("Host is up and responding, but does not support http get")
                return
        except r.exceptions.ConnectionError as e:
            print(
                "Failure connecting to load balancer, may not be running yet {}".format(
                    request_url
                )
            )


def update_service(task_defintion_arn: str, subnets: list):
    print(
        "Updating {} service on {} cluster, with task definition arn {}".format(
            CLUSTER_NAME, SERVICE_NAME, task_defintion_arn
        )
    )

    response = get_ecs_client().update_service(
        cluster=CLUSTER_NAME,
        service=SERVICE_NAME,
        # serviceName=SERVICE_AND_TASK_NAME, NOTE: create_service has a different parameter here than update_service, but it's the same value
        taskDefinition=task_defintion_arn,
        forceNewDeployment=True,
    )

    print(response)

    return response["service"]["serviceArn"]


def create_service(task_defintion_arn: str, subnets: list, target_group_arn: str):
    ecs_client = get_ecs_client()

    print(
        "Utilizing cluster '{}' to create service {}".format(CLUSTER_NAME, SERVICE_NAME)
    )

    response = ecs_client.describe_services(
        cluster=CLUSTER_NAME, services=[SERVICE_NAME]
    )

    if len(response["services"]) >= 2:
        raise ValueError(
            "There are multiple services running. The DevOps scripts needs to be extended to support this. Erroring out"
        )
    # if len(response['services']) >= 1 and response['services'][0]['status'] == 'DRAINING':
    #     raise ValueError("The previous version of the service is being drained probably from a previous deletion call. Need to rerun once draining is complete")
    # TODO Implement auto-retry
    if len(response["services"]) >= 1 and response["services"][0]["status"] == "ACTIVE":
        if (
            response["services"][0]["runningCount"]
            < response["services"][0]["desiredCount"]
        ):
            print(
                "There are not enough tasks running in the service, it might be in a bad state. Will continue to update anyway."
            )

        print(
            "Service {} already exists. Arn for service {}".format(
                SERVICE_NAME, response["services"][0]["serviceArn"]
            )
        )
        return update_service(task_defintion_arn, subnets)

    response = ceate_service(response, subnets, target_group_arn, task_defintion_arn)
    return response["service"]["serviceArn"]


def ceate_service(response, subnets, target_group_arn, task_defintion_arn):
    response = get_ecs_client().create_service(
        cluster=CLUSTER_NAME,
        serviceName=SERVICE_NAME,
        taskDefinition=task_defintion_arn,
        desiredCount=TASK_COUNT,
        launchType="FARGATE",
        deploymentConfiguration={"maximumPercent": 200, "minimumHealthyPercent": 100},
        # Network configuration is required as we're using FARGATE tasks
        # which require the configuration below
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": subnets,
                "securityGroups": [get_security_group_id()],
                "assignPublicIp": "ENABLED",  # |'DISABLED'
            }
        },
        loadBalancers=[
            {
                "targetGroupArn": target_group_arn,
                # 'loadBalancerName': SERVICE_AND_TASK_NAME,
                # Can't use the 2 above parameters at the same time. Fargate uses a target group
                # concept to add/remove instances
                "containerName": SERVICE_NAME,
                "containerPort": DEFAULT_PORT,
            },
        ],
    )
    return response


def run_task():
    ecs_client = get_ecs_client()
    response = ecs_client.run_task(
        taskDefinition=SERVICE_NAME,
        launchType="FARGATE",
        cluster=CLUSTER_NAME,
        platformVersion="LATEST",
        count=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": get_public_subets_arns(),
                "securityGroups": [get_security_group_id()],
                "assignPublicIp": "ENABLED",  # |'DISABLED'
            }
        },
    )
    print(response)


def verify_deployed():
    ecs_session = get_ecs_client()
    ## Task Definition
    families = ecs_session.list_task_definition_families()
    families = list(filter(lambda x: SERVICE_NAME == x, families["families"]))

    if len(families) != 1 and families[0] != SERVICE_NAME:
        raise ValueError("There is no task family name with {}".format(SERVICE_NAME))

    check_task_count(ecs_session, families)


def check_task_count(ecs_session, families):
    tasks = ecs_session.list_tasks(
        cluster=CLUSTER_NAME,
        # containerInstance='string',
        family=families[0],
        # nextToken='string',
        # maxResults=123,
        # startedBy='string',
        # serviceName='string',
        # desiredStatus='RUNNING'|'PENDING'|'STOPPED',
        # launchType='EC2'|'FARGATE'|'EXTERNAL'
    )

    if len(tasks["taskArns"]) < TASK_COUNT:
        print(
            "It seems that there aren't enough tasks running for {}; {}".format(
                CLUSTER_NAME, SERVICE_NAME
            )
        )

    await_load_balancer(load_balancer_arn=get_load_balancer_arn())
    # Check service running
    services = get_ecs_client().describe_services(
        cluster=CLUSTER_NAME, services=[SERVICE_NAME]
    )
    service = services["services"][0]
    # Check active & number of tasks matches above
    if service["status"] != "ACTIVE":
        raise ValueError(
            "Service {} is not in an ACTIVE state {}".format(
                SERVICE_NAME, service["status"]
            )
        )

    for i in range(20):
        tasks = ecs_session.list_tasks(cluster=CLUSTER_NAME, family=families[0])

        if len(tasks["taskArns"]) == TASK_COUNT:
            return

    services = get_ecs_client().describe_services(
        cluster=CLUSTER_NAME, services=[SERVICE_NAME]
    )
    service = services["services"][0]

    if service["runningCount"] < TASK_COUNT:
        raise ValueError(
            "Service is running {} tasks, but desired count is {}. There could be an issue".format(
                service["runningCount"], TASK_COUNT
            )
        )


def delete_listener(load_balancer_arn):
    listner_arn = get_listener_arn(load_balancer_arn, DEFAULT_PORT)

    if listner_arn is None:
        print("There is no listener to delete")
        return

    get_elb_client().delete_listener(ListenerArn=listner_arn)


def delete_load_balancer(load_balancer_arn):
    if load_balancer_arn is None:
        print("There is no load balancer to delete")
        return

    get_elb_client().delete_load_balancer(LoadBalancerArn=load_balancer_arn)


def delete_target_group():
    target_group_arn = get_target_group_arn(DEFAULT_PORT)

    if target_group_arn is None:
        print("There is no target group to delete")
        return

    get_elb_client().delete_target_group(TargetGroupArn=target_group_arn)


def delete_service():
    ecs_session = get_ecs_client()

    try:
        get_ecs_client().delete_service(
            cluster=CLUSTER_NAME, service=SERVICE_NAME, force=True
        )
    except ecs_session.exceptions.ServiceNotFoundException as e:
        print("No service called {} to delete".format(SERVICE_NAME))


def delete_all():
    load_balancer_arn = get_load_balancer_arn()
    delete_listener(load_balancer_arn)
    # delete_load_balancer(load_balancer_arn)
    delete_target_group()
    delete_service()


def full_build(create: bool = False, teardownService: bool = True):
    ecs_session = get_ecs_client()

    if teardownService:
        delete_all()

    if create and is_any_clusters(ecs_session):
        cluster_arn = get_cluster_arn(ecs_session)
        print("Cluster ARN: {}".format(cluster_arn))

        task_arn = create_task_definition()
        subnets = get_public_subets_arns()

        target_group_arn = create_target_group()
        load_balancer_arn = create_load_balancer()
        # import time
        # print("Waiting for load balancer to be created until adding the listener")
        # time.sleep(60)
        listener_arn = attach_load_balancer_and_target_group(
            target_group_arn, load_balancer_arn
        )

        await_load_balancer(load_balancer_arn=load_balancer_arn)

        fargate_service_arn = create_service(task_arn, subnets, target_group_arn)

        verify_deployed()


if __name__ == "__main__":
    full_build(False, True)
