# Open API with AWS EMR and Jupyter :hand: fa18-516-22

| Ian Sims
| isims@iu.edu
| Indiana University
| hid: fa18-516-22
| github: [:cloud:](https://github.com/cloudmesh-community/fa18-516-22/project-report/report.md)
| code: [:cloud:](https://github.com/cloudmesh-community/fa18-516-22/project-code/README.md)

**:mortar_board: Learning Objectives**

* Use an Open API to interact with various AWS products
* Learn to deploy an AWS EMR Cluster
* Interact with Jupyter notebooks stored in S3 buckets

## Introduction

### Open API

Rest API's allow for the creation of services that can interact with multiple applications. This project will seek to develop an API for interacting with various AWS products. These products include AWS EMR and S3. In addition, these APIs will be hosted on an AWS EC2 instance.

Open API is and open source project intended to create a consistent format for creating REST services. Open API descripes this project as:

> "The OpenAPI Initiative (OAI) was created by a consortium of forward-looking industry experts who recognize the immense value of standardizing on how REST APIs are described." [@fa18-516-22-OpenAPI]

### AWS EMR

EMR is an Amazon product that allows for the creation of clusters of Elastic Compute Cloud (EC2) instances. EMR allows user to take advantage of distributed computing capabilities. As the name suggests this product is designed to allow users to easily scale their cluster to meet their computing needs.

EMR clusters can be created through relatively simple web interfaces or can be created through code using CLI. EMR Clusters can be configured for size and can be provisioned with open-source distributed frameworks such as SPARK and HBase.

For this project we will interact with EMR using an API. This API will allow for the creationand termination of an EMR cluster. It will also allow a user to retrieve the status of an EMR cluster. This EMR cluster will also include the installation of Jupyter Hub to enable the development of notebooks for analytical purposes.

### AWS EC2

EC2 is an Amazon product that enables cloud computing. Amazon describes this product as:

> "Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers." [@fa18-516-22-AWSEC2]

For this project APIs will be hosted on an EC2 instance.

### AWS S3

S3 is one of Aamzon's data storage solutions. For this project we will configure an EMR cluster to read/write to an S3 bucket. This bucket would potentially be used for accessing data for analytical purposes and to store log files associated with the cluster. In addition, the Jupyter Hub instance installed on the EMR cluster will store created notebooks on S3. This will allow for terminating the cluster when it is not in use with the ability to retrieve saved notebooks for future use.

### JupyterHub

JupyterHub is an open-source project intended to allow a wide range of users to interact with and organize notebooks for analysis. The open-source project describes JupyterHub as follows:

> "JupyterHub brings the power of notebooks to groups of users. It gives users access to computational environments and resources without burdening the users with installation and maintenance tasks. Users - including students, researchers, and data scientists - can get their work done in their own workspaces on shared resources which can be managed efficiently by system administrators." [@fa18-516-22-JupyterHub]

For this project we will build an API that creates an Amazon EMR cluster that includes an installation of JupyterHub.

## Implemenation

### Setting up AWS CLI

After setting up an AWS account account: [AWS Account](https://github.com/cloudmesh-community/book/blob/master/chapters/iaas/aws/aws.md#creating-an-account) and an [AWS Key Pair](https://github.com/cloudmesh-community/book/blob/master/chapters/iaas/aws/aws.md#setting-up-key-pair), I needed to be able to work with AWS products from the command line. To do this I utilized the AWS Command-Line Interface (CLI) from a Linux envirionment.

First I set up a [Linux](https://github.com/cloudmesh-community/book/blob/master/chapters/linux/linux.md) environment using VirtualBox. I then installed [Python](https://github.com/cloudmesh-community/book/blob/master/chapters/prg/python/python-install.md) and [PIP](https://pip.pypa.io/en/stable/installing/) on that environment. Finally I installed CLI using the following Bash command:

```bash
$ pip install awscli
```
The following item had to be configured for CLI:

* AWS Access Key ID
* AWS Secret Access Key
* Default region name (this is the default region that will be used when you create EC2 instances)
* Default output format (the default format is json)

### Setting up AWS Admin Access

In order to work form the command line with various AWS products I had to set up admin access. Using CLI I ran the following commands:

```bash
$ aws iam create-group --group-name Admins
```

```bash
$ aws iam attach-group-policy --group-name Admins --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

Then through the AWS Console I assigned myself to the admin group.

Under 'Group Actions', select 'Add Users to Group'
<br><br>
+@fig:aws-api-1
[@fa18-516-22-AWS-Security-1]

![AWS Security [@fa18-516-22-AWS-Security-1]](images/aws-api-1.png){#fig:aws-api-1}
<br><br>
### Creating and Configuring EC2 Instance to Host API

#### EC2 Security Group

To set up the EC2 instance for hosting my API I first used the Amazon Console to set up a security group.

Navigating to: [EC2 Security Group](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#SecurityGroups:sort=groupId)

Select 'Create Security Group'
<br><br>
+@fig:aws-api-2
[@fa18-516-22-AWS-Security-2]

![AWS Security [@fa18-516-22-AWS-Security-2]](images/aws-api-2.png){#fig:aws-api-2}
<br><br>
I then gave the security group a name, selected the default VPC and added two rules. One that opens port 8080 for http traffic and one to allow ssh access from my computer. Port 8080 will be used for the API.
<br><br>
+@fig:aws-api-3
[@fa18-516-22-AWS-Security-3]

![AWS Security [@fa18-516-22-AWS-Security-3]](images/aws-api-3.png){#fig:aws-api-3}
<br><br>
#### EC2 Create Instance

Now it was time to create the EC2 instance using the AWS Console: [Launch EC2](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#Instances:sort=instanceId)

Click the 'Launch Instance' button:
<br><br>
+@fig:aws-api-4
[@fa18-516-22-AWS-EC2-1]

![AWS EC2 [@fa18-516-22-AWS-EC2-1]](images/aws-api-4.png){#fig:aws-api-4}
<br><br>
Select the Ubuntu version. In this case I used 18.04:
<br><br>
+@fig:aws-api-5
[@fa18-516-22-AWS-EC2-1]

![AWS EC2 [@fa18-516-22-AWS-EC2-1]](images/aws-api-5.png){#fig:aws-api-5}
<br><br>
Select a small instance type and go to "Next: Configure Instance Details:
<br><br>
+@fig:aws-api-6
[@fa18-516-22-AWS-EC2-1]

![AWS EC2 [@fa18-516-22-AWS-EC2-1]](images/aws-api-6.png){#fig:aws-api-6}
<br><br>
Make sure the default VPC is selected and then go to 'Configure Security Group':
<br><br>
+@fig:aws-api-7
[@fa18-516-22-AWS-EC2-1]

![AWS EC2 [@fa18-516-22-AWS-EC2-1]](images/aws-api-7.png){#fig:aws-api-7}
<br><br>

Click 'Select and existing security group' and select the group created earlier:
<br><br>
+@fig:aws-api-8
[@fa18-516-22-AWS-EC2-1]

![AWS EC2 [@fa18-516-22-AWS-EC2-1]](images/aws-api-8.png){#fig:aws-api-8}
<br><br>
You can now review and launch the instance.

#### EC2 SSH

I then went into to my local Linux environment and set up a key pair to enable ssh to my EC2 instance. I did this using CLI and the following commands:

```bash
$ aws ec2 create-key-pair --key-name dlec2-key --query 'KeyMaterial' --output text > dlec2-key.pem
```

Allow access to the key:
```bash
$ chmod 400 dlec2-key.pem
```

Then locating the 'Public DNS' at: [AWS EC2](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#Instances:sort=instanceId), I connected to the EC2 instance with the following command:

```bash
$ ssh -i "dlec2-key.pem" ubuntu@ec2-18-191-50-79.us-east-2.compute.amazonaws.com
```

#### EC2 Set Up

Now I needed to set up a Python virtual environment for my rest service:

```bash
$ pyenv install -l
$ pyenv install 3.6.6
$ pyenv virtualenv 3.6.6 RestService
$ pyenv activate RestService
```

Install AWS CLI

```bash
$ pip install awscli
```
The following items had to be configured for CLI:

* AWS Access Key ID
* AWS Secret Access Key
* Default region name (this is the default region that will be used when you create EC2 instances)
* Default output format (the default format is json)

### Create S3 Storage

In order to store analytical data and to backup my Jupyter notebooks I created to S3 buckets using the following commands:

```bash
$ aws s3 mb s3://e516-analytical-datasets --region us-east-2
$ aws s3 mb s3://e516-jupyter-backup --region us-east-2
```

### Codegen Set Up

#### Install Java

I used Codegen to create my rest service and Java ia a requirement. I installed Java using the following commands:

```bash
$ sudo apt update
$ sudo apt install default-jre
$ sudo apt install default-jdk
```

#### Install Codegen

I ran the following commands for installation:

```bash
$ mkdir ~/e516/swagger
$ cd ~/e516/swagger
$ wget https://oss.sonatype.org/content/repositories/releases/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar
```

I then opened the .bashrcls file and added an alias for codegen:

```bash
$ alias swagger-codegen="java -jar ~/e516/swagger/swagger-codegen-cli-2.3.1.jar"
```

### Building the Rest Service

Using Swagger I build my API specs. This API has POST, DELETE, and GET methods. The POST method will create an AWS EMR cluster and install Jupyter Hub. The DELETE method allows for the termination of the cluster. The GET method retrieves information about the cluster including the status and a link to the Jupyter Hub web ui.

```yaml
swagger: "2.0"
info:
  version: "0.0.1"
  title: "emrinfo"
  description: "API to spin up an AWS EMR cluster, to check status, and to terminate."
  termsOfService: "http://swagger.io/terms/"
  contact:
    name: "EMR Rest Service"
  license:
    name: "Apache"
host: 18.191.50.79:8080
basePath: /api
schemes:
  - http
consumes:
  - "application/json"
produces:
  - "application/json"
paths:
  /emr/create/{num_of_nodes}:
    post:
      summary: Create EMR cluster.
      parameters:
        - in: path
          name: num_of_nodes
          required: true
          type: integer
          minimum: 1
          description: The number of nodes in the cluster
      responses:
        200:
          description: OK
  /emr/info/{cluster_id}:
    get:
      summary: Returns EMR cluster Info.
      parameters:
        - in: path
          name: cluster_id
          required: true
          type: string
          minimum: 1
          description: The cluster id for EMR
      responses:
        200:
          description: OK
  /emr/terminate/{cluster_id}:
    delete:
      summary: Deletes EMR cluster.
      parameters:
        - in: path
          name: cluster_id
          required: true
          type: string
          minimum: 1
          description: The cluster id for EMR
      responses:
        200:
          description: OK
definitions:
  EMR:
    type: "object"
    required:
      - "model"
    properties:
      model:
        type: "string"
```





## Conclusion

