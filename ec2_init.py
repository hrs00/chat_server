#!/usr/bin/python3

import boto3
import json
import time

ec2 = boto3.client("ec2")
iam = boto3.client("iam")
ec2_res = boto3.resource("ec2")
keypair_name = input("Enter KeyPair name: ")
s3_bucket = input("Enter S3 bucket name: ")

user_data = """#!/bin/bash
sudo apt update -y
sudo apt install -y python3
sudo aws s3 cp s3://{}/server.py .
sudo python3 server.py""".format(s3_bucket)

vpc = ec2.describe_vpcs()
vpc_id = vpc["Vpcs"][0]["VpcId"]
security_group = ec2.create_security_group(
        Description="chat_server",
        GroupName="chat_server_sg",
        VpcId = vpc_id
    )
sg_id = security_group["GroupId"]
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
        "IpProtocol": "TCP",
        "FromPort": 5555,
        "ToPort": 5555,
        "IpRanges": [{
            'CidrIp': "0.0.0.0/0"
        }]},
        {
        "IpProtocol": "TCP",
        "FromPort": 22,
        "ToPort": 22,
        "IpRanges": [{
            'CidrIp': "0.0.0.0/0"
        }]}
    ])

assume_role_policy_document = json.dumps({
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Principal": {"Service": "ec2.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }
})

iam.create_role(
    RoleName = "s3_access",
    AssumeRolePolicyDocument = assume_role_policy_document
    )

iam.attach_role_policy(
    RoleName="s3_access",
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess")

iam.create_instance_profile(InstanceProfileName="csrv")

waiter = iam.get_waiter("instance_profile_exists")
waiter.wait(InstanceProfileName="csrv",WaiterConfig={"Delay": 4})

iam.add_role_to_instance_profile(
    InstanceProfileName="csrv",
    RoleName="s3_access")

waiter = iam.get_waiter("instance_profile_exists")
waiter.wait(InstanceProfileName="csrv",WaiterConfig={"Delay": 4})

iam_inst = iam.get_instance_profile(
        InstanceProfileName="csrv"
        )

iam_inst_arn = iam_inst["InstanceProfile"]["Arn"]

time.sleep(121)

instances = ec2_res.create_instances(
        ImageId="ami-04e81c5c7a4851ebf",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        UserData=user_data,
        KeyName=keypair_name,
        SecurityGroupIds=[sg_id],
        IamInstanceProfile={
        "Arn": iam_inst_arn
    })

instance_id = instances[0].instance_id

waiter = ec2.get_waiter('instance_status_ok')
waiter.wait(InstanceIds = [instance_id])

instances = ec2.describe_instances(InstanceIds=[instance_id])

print("chat_server's IP address: ", end="")
print(instances["Reservations"][0]["Instances"][0]["PublicIpAddress"])
