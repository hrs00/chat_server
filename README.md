<p align="center"><img src="https://github.com/hrs00/chat_server/assets/135930294/59321727-3830-4764-8120-ca7e440c4cfd"></p>

## About

chat_server is a program that is built to be hosted on AWS EC2 instance and lets client access a text-based interface to talk with other clients connected to chat_server over TCP. The repository has an EC2 initialization script that creates EC2 instance with all it's required components.

## Requisites

It requires a free-tier AWS account to host the chat server and <a href="https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"> AWS CLI installed</a>. Then <a href="https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html">create access keys</a> in AWS console and use them to <a href="https://aws.amazon.com/getting-started/guides/setup-environment/module-three/">configure AWS CLI</a>.

<a href="https://www.python.org/downloads/">Python3</a> and <a href="https://pypi.org/project/boto3/">boto3</a> module also needs to be installed.


## Installation

### 1. Create a Key pair

Run the following command to create a key pair and save it in the current working directory. The .pem file can be used to connect to the EC2 instance via SSH.
You can save it in .ppk file if you want to use PuTTY to connect.

```bash
 aws ec2 create-key-pair --key-name chat_server --query 'KeyMaterial' --output text > chat_server.pem
```

### 2. Create a S3 bucket

Run the following command to create a S3 bucket named cserver.

```bash
aws s3api create-bucket --bucket cserver --acl private --region us-east-1
```


If you want to create a S3 bucket in any other region replace <region-code> in the following command and run. Refer to <a href="https://docs.aws.amazon.com/general/latest/gr/rande.html#region-names-codes">this</a> for region names and their respective region codes. 

```bash
aws s3api create-bucket --bucket cserver --acl private --create-bucket-configuration LocationConstraint="<region-code>" --region <region-code>
```

### 3. Upload server.py to the S3 bucket

The following command uploads server.py file to the cserver bucket.
 
```bash
aws s3 cp /path/to/server.py s3://cserver/server.py
```
Check for server.py in cserver bucket.

```bash
aws s3 ls s3://cserver/
```
![image](https://github.com/hrs00/chat_server/assets/135930294/693794b6-58d9-4aa7-aa97-454f67279684)

### 4. Run EC2 initialization script

Run the following:

```bash
/path/to/ec2_init.py
```
Enter the key pair name and S3 bucket name.

![image](https://github.com/hrs00/chat_server/assets/135930294/0fb1fdc5-3482-4e1f-a247-1a2d5995fb60)
  
It will print IP address of the chat_server.

![image](https://github.com/hrs00/chat_server/assets/135930294/a7ebe18c-f348-40cb-b5bf-6a3f155ba69e)
 
The python script uses boto3 module to create EC2 instance and it's assosciated security group and IAM role.
This script needs to run only once. Running it again will throw errors. 
  
### 5. Run the client

Run client.py using the following command

```bash
python3 /path/to/client.py
```
 
![image](https://github.com/hrs00/chat_server/assets/135930294/e31153cd-9888-4ae2-abcf-fdb9c2f98119)

Enter the IP address of chat_server.

  
![image](https://github.com/hrs00/chat_server/assets/135930294/4492454b-819f-451f-bd64-4a345904eca1)

## Usage:
  
### Register to create new account:

![image](https://github.com/hrs00/chat_server/assets/135930294/5f5d17d4-5976-4514-97d5-da8371b1be60)

  
### Login:
  
![image](https://github.com/hrs00/chat_server/assets/135930294/9cbd7b7f-1ba5-4a0f-9966-c39ded2780f5)


### Exit during Registration/Login process:
  
![image](https://github.com/hrs00/chat_server/assets/135930294/3322b3e0-8241-478d-85ee-32a4422dbf01)


### Ctrl + C to quit:
 
![image](https://github.com/hrs00/chat_server/assets/135930294/296fc662-c830-4b97-9808-d0fadc774046)


  













