from fintekkers.devops.aws_account_setup import get_ecr_client
from fintekkers.devops.aws_account_setup import REPOSITORY_NAME, SERVICE_NAME, CLUSTER_NAME
import base64, os 

from docker import DockerClient
from docker.models.images import Image
from strip_ansi import strip_ansi

DOCKER_FILE = os.environ['FINTEKKERS_DOCKER_FILE'] if 'FINTEKKERS_DOCKER_FILE' in os.environ else "Dockerfile"
print("DOCKER_FILE: {}".format(DOCKER_FILE))

DOCKER_IMAGE_VERSION = os.environ['FINTEKKERS_DOCKER_IMAGE_VERSION'] if 'FINTEKKERS_DOCKER_IMAGE_VERSION' in os.environ else "0"
print("DOCKER_IMAGE_VERSION: {}".format(DOCKER_IMAGE_VERSION))

def get_image_tag_name():
    return SERVICE_NAME

def get_image_tag_name_with_version():
    return "{}:{}".format(get_image_tag_name(), "latest")

import docker
import subprocess

def docker_login() -> tuple:
    ecr_credentials = (get_ecr_client().get_authorization_token()['authorizationData'][0])

    ecr_username = 'AWS'

    ecr_password = (
        base64.b64decode(ecr_credentials['authorizationToken'])
        .replace(b'AWS:', b'')
        .decode('utf-8'))

    ecr_url = ecr_credentials['proxyEndpoint'].replace("https://", "")


    # token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(ecr_credentials['authorizationToken']).decode().split(':')
    registry = ecr_url

    # loggin in via the docker sdk doesnt work so we're gonna go with this workaround
    command = 'docker login -u %s -p %s %s' % (username, password, registry)

    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.communicate()

    print("Logging in to {}. {} / {}".format(ecr_url, ecr_username, "Password Omitted"))

    docker_client = docker.from_env()
    login_status = docker_client.login(username=ecr_username, password=ecr_password, registry=ecr_url)

    print("ECR docker login status: {}".format(login_status['Status']))
    #Equivalent of aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 754996918532.dkr.ecr.us-east-1.amazonaws.com

    # docker_client = docker.from_env()
    return docker_client, ecr_url

def build_image(docker_client:DockerClient, image_tag_name:str):
    #If you're building on Mac M chips, or on Windows, you'll need this platform arg.
    #equivalent of " --platform linux/amd64" param when running docker build on command line
    # print("Building image: {}".format(image_tag_name))
    # image, build_log = docker_client.images.build(path='.', tag=image_tag_name, \
    #     rm=True, dockerfile=DOCKER_FILE, platform="linux/amd64", nocache=True)
    # print(list(build_log)[:-5])

    import json

    docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')

    #Currently forcing the platform to be linux/amd64. This is the platform used by Amazon Linux Os images
    #on Fargate runtimes. May need more flexibility in the future
    generator = docker_client.build(path='.', tag=image_tag_name, platform="linux/amd64", nocache=True)
    last_message = ""

    while True:
        try:
            output = generator.__next__()
            #Output is a binary string so decode it. Inside can be multiple JSON
            #blocks, so we split by the line separator
            output:list = output.decode('utf8').split('\r\n')

            for line in output:
                #Each line should be a valid JSON value so we load it and get the stream
                #value which is what the docker CLI is outputting.
                if len(line) == 0:
                    continue #Nothing here...

                json_output = json.loads(line)
                if 'stream' in json_output:
                    stream_value = json_output['stream']

                    #this is essentially an empty string and ignore
                    if len(stream_value) == 1 and len(stream_value.strip('\n')) == 0:
                        continue

                    #TODO: This kind of sucks because the stream is encoded in something else. Need
                    #to encode and decode perhaps
                    if len(stream_value) > 0:
                        #The stream can contain ASNI escape characters, e.g. color coding information
                        #for windows machines. So we strip them before printing. Anniying!
                        last_message = strip_ansi(json_output['stream']).strip('\n')
                        print(last_message)
        except StopIteration:
            if "error: failed" in last_message:
                print("********** FAILURE TO BUILD********")
            print("Docker image build complete")
            break
        except ValueError:
            #The logic above does not handle this line of output
            print("Error parsing output from docker image build: %s" % output)

def build_and_tag_image(docker_client:DockerClient, image_tag_name:str, versions:list, ecr_url:str):
    #This will build the image using the docker api
    build_image(docker_client=docker_client, image_tag_name=image_tag_name)

    ecr_repo_name = '{}/{}'.format(ecr_url.replace('https://', ''), REPOSITORY_NAME)

    ## Returns: dict [Id = sha...., RepoTags [fintekkers-broker-service:latest, etc]
    image:Image = docker.from_env().images.get(image_tag_name)

    for version in versions:
        print("Tagging image with {}, version {}".format(ecr_repo_name, version))
        tmp_image_name = "{}:{}".format(ecr_repo_name, version)
        image.tag(tmp_image_name)

    return ecr_repo_name
    
def push_image(docker_client:DockerClient, ecr_repo_name:str, versions:list):
    print("Pushing image: {}".format(ecr_repo_name))

    for version in versions:
        push_log = docker_client.images.push(ecr_repo_name, tag=version)
        #Equivalent of docker push 754996918532.dkr.ecr.us-east-1.amazonaws.com/fintekkers-dummy-service:latest
        print(push_log)


import subprocess

def _run_command(command:str):
    print(f"Running command: {command}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error is not None:
        print(f"Error: {error}")
    else:
        print(f"No errors were encountered while running {command}")

def build_and_push_docker_image():
    #TODO - fix this
    SERVICE_NAME = os.environ['FINTEKKERS_SERVICE_NAME'] if 'FINTEKKERS_SERVICE_NAME' in os.environ \
        else "{}-dummy-service".format(CLUSTER_NAME)
    print("SERVICE_NAME: {}".format(SERVICE_NAME))

    _run_command('aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 754996918532.dkr.ecr.us-east-1.amazonaws.com')
    _run_command(f'docker build --platform linux/amd64 -t {SERVICE_NAME} .')
    _run_command(f'docker tag {SERVICE_NAME}:latest 754996918532.dkr.ecr.us-east-1.amazonaws.com/{SERVICE_NAME}:latest')
    _run_command(f'docker push 754996918532.dkr.ecr.us-east-1.amazonaws.com/{SERVICE_NAME}:latest')


def build_and_push_docker_image_old():
    image_tag_name = get_image_tag_name()

    versions_for_this_build = ["latest", DOCKER_IMAGE_VERSION]

    docker_client, ecr_url = docker_login()
    print("ECR repository is: {}".format(ecr_url))

    # for version in versions_for_this_build:
    ecr_repo_name = build_and_tag_image(docker_client, image_tag_name, versions_for_this_build, ecr_url)
    print("Pushing image to {}".format(ecr_repo_name))
    push_image(docker_client, ecr_repo_name, versions_for_this_build)

if __name__ == "__main__":
    build_and_push_docker_image()