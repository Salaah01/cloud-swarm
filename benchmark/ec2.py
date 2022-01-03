"""Functions related to managing EC2 instances."""

import typing as _t
import os
import subprocess
import threading
import boto3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SETUP_SCRIPT = os.path.join(BASE_DIR, 'server_setup.sh')

IMAGE_ID = 'ami-0015a39e4b7c0966f'  # Ubuntu Server 20.04 LTS
INSTANCE_TYPE = 't2.micro'
SECURITY_GROUPS = ['sg-0181cc2e6e7afc2d3']

ec2 = boto3.resource('ec2')


def create_instances(
    num_instances=1,
    image_id=IMAGE_ID,
    instance_type=INSTANCE_TYPE,
    key_name='ec2-key-pair'
) -> _t.List:
    """Creates EC2 instances
    Args:
        num_instances (int): Number of instances to create
        image_id (str): AMI ID
        instance_type (str): Instance type
        key_name (str): Name of the key pair
    Returns:
        list: List of instances
    """
    instances = ec2.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=num_instances,
        MaxCount=num_instances,
        KeyName=key_name,
    )

    # Setup each instance in a separate thread
    threads = []
    for instance in instances:
        t = threading.Thread(target=_setup_instance, args=(instance,))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    return instances


def terminate_instances(instances) -> None:
    """Terminates the instances
    Args:
        instances (list): List of instances to terminate
    Returns:
        None
    """
    print('\033[92mTerminating instances\033[0m')
    for instance in instances:
        instance.terminate()

    for instance in instances:
        instance.wait_until_terminated()
    print('\033[92mTerminated instances\033[0m')

def _setup_instance(instance) -> None:
    """Setups the instance by running a setup script once it is ready.
    Args:
        instance (boto3.resources.ec2.Instance): Instance to setup
    Returns:
        None
    """
    print(f'\033[92mSetting up {instance.id}\033[0m')
    instance.wait_until_running()

    # Add the instance to a security group that allows SSH access
    instance.modify_attribute(Groups=SECURITY_GROUPS)

    # Run the setup script
    exit_code = subprocess.call([
        'bash',
        SERVER_SETUP_SCRIPT,
        instance.public_ip_address
    ])
    if exit_code != 0:
        raise Exception(
            f'\033[91m{instance.id} setup failed with exit code {exit_code}\033[0m'  # noqa: E501
        )

    print(f'\033[92mFinished setting up {instance.id}\033[0m')
