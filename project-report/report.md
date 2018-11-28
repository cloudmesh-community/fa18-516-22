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
pip install awscli
```
The following item had to be configured for CLI:

* AWS Access Key ID
* AWS Secret Access Key
* Default region name (this is the default region that will be used when you create EC2 instances)
* Default output format (the default format is json)

### Setting up AWS Admin Access

In order to work form the command line with various AWS product I had to set up admin access. Using CLI I ran the following commands:

```bash
aws iam create-group --group-name Admins
```

```bash
aws iam attach-group-policy --group-name Admins --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

Then through the AWS Console I assigned myself to the admin group.

Under 'Group Actions', select 'Add Users to Group'

+@fig:aws-api-1
[@fa18-516-22-AWS-Security-1]

![AWS Security [@fa18-516-22-AWS-Security-1]](images/aws-api-1.png){#fig:aws-api-1}







This is done through the AWS console: [AWS IAM](https://console.aws.amazon.com/iam/home?region=us-east-2#/users).

On the users tab I clicked 'Add user':

+@fig:aws-api-1
[@fa18-516-22-AWS-Security-1]

![AWS Security [@fa18-516-22-AWS-Security-1]](images/aws-api-1.png){#fig:aws-api-1}

Give the user a name and click 'Next:Permissions':

+@fig:aws-api-2
[@fa18-516-22-AWS-Security-2]

![AWS Security [@fa18-516-22-AWS-Security-2]](images/aws-api-2.png){#fig:aws-api-2}


## Conclusion

