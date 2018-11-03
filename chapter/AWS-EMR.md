# AWS Elastic Map Reduce (EMR) :o:

---

**:mortar_board: Learning Objectives**

* Learn about EMR
* Deploy an EMR cluster using:
  - Amazon's Command Line Interface (CLI)
  - Amazon's Web Interfaces
* Run an example Spark application on an EMR cluster

---

## Introduction

EMR is an Amazon product that allows for the creation of clusters of Elastic Compute Cloud (EC2) instances. EMR allows user to take advantage of distributed computing capabilities. As the name suggests this product is designed to allow users to easily scale their cluster to meet their computing needs.

EMR clusters can be created through relatively simple web interfaces or can be created through code using CLI. EMR Clusters can be configured for size and can be provisioned with open-source distributed frameworks such as SPARK and HBase.

## Prerequisites

* [AWS Account](https://github.com/cloudmesh-community/book/blob/master/chapters/iaas/aws/aws.md#creating-an-account)

* [AWS Key Pair](https://github.com/cloudmesh-community/book/blob/master/chapters/iaas/aws/aws.md#setting-up-key-pair)

* [Install and Configure AWS CLI](https://github.com/cloudmesh-community/fa18-516-22/blob/master/section/AWS-CLI.md)

* [AWS Admin Access](https://github.com/cloudmesh-community/fa18-516-22/blob/master/section/AWS-Admin-Access.md)

* [Linux Environment](https://github.com/cloudmesh-community/book/blob/master/chapters/linux/linux.md)

## Creating EMR Cluster Using CLI

### Create Security Roles
In this example we will use the default EMR security roles. These roles enable the nodes within the cluster to access each other and to access other AWS products.

```bash
aws emr create-default-roles
```

### Setting up authentication
In this example we will be using Kerberos for authentication. The Kerberos configuration would allow you to add additional users to your EMR cluster.

Create a json file with the following content and save to a local file:
```bash
{
  "AuthenticationConfiguration": {
    "KerberosConfiguration": {
      "Provider": "ClusterDedicatedKdc",
      "ClusterDedicatedKdcConfiguration": {
        "TicketLifetimeInHours": 24
      }
    }
  }
}
```

Create the Kerberos configuration using the previously created json file:
```bash
aws emr create-security-configuration --name "KerberosSecurityConfiguration" --security-configuration file://MyKerberosSecurityConfig.json
```
### Determine the applicable subnet
The EMR cluster will run on a subnet so you need to determine the appropriate subnet for you availability zone. You will need to enter your default zone in the code below.

```bash
aws ec2 describe-subnets --filters "Name=availabilityZone,Values=us-east-2b"
```
The applicable information is returned as the "SubnetId" field.

### Create the EMR cluster
In this example we will create a simple cluster with 3 nodes. One master node and two slave nodes. We will also specify the EC2 instance type (m4.large).  These parameters are configurable and you can create larger clusters with more processing power. There are multiple EMR versions available, this example uses the latest version available at the time of creation.

There are a variety of applications that can be installed on the EMR cluster at creation, but in this case we will simply install Spark. The Kerberos password can be used to add users to your cluster once it is created. The KeyName is your EC2 key pair that is referenced in the Prerequisites section.

```bash
aws emr create-cluster --name "Test-Kerberized-Spark-Cluster" \
--release-label emr-5.17.0 \
--instance-type m4.large \
--instance-count 3 \
--use-default-roles \
--ec2-attributes KeyName=your-key,SubnetId=your-subnet-id \
--security-configuration KerberosSecurityConfiguration \
--applications Name=Spark \
--kerberos-attributes Realm=EC2.INTERNAL,KdcAdminPassword=your-password
```

### Check the status of your cluster
The cluster may take several minutes to initialize. To check the status of your cluster use the cluster-id that was returned in the previous step.

```bash
aws emr describe-cluster --cluster-id your-cluster-id
```

### Terminate your cluster
To terminate your cluster use the following command (hint: AWS charges apply while your cluster is up).

```bash
aws emr terminate-clusters --cluster-ids your-cluster-id
```
## Creating EMR Cluster Using AWS Web Console

### Set up authentication

Go to the AWS Console (ensure that the URL references your default region)

https://us-east-2.console.aws.amazon.com/elasticmapreduce/home?region=us-east-2#

Select the "Security configurations" and click "Create". Give a meaningful name like: "KerberosSecurityConfiguration". Then select "Kerberos" under "Authentication" and click "Create".

### Create the EMR cluster

Go to the AWS Console (ensure that the URL references your default region)

https://us-east-2.console.aws.amazon.com/elasticmapreduce/home?region=us-east-2#

Click "Create cluster"

Go to "Advanced Options" and:
* Select your desired EMR version
* Select Spark
* Click "Next"
* Select your desired instance types
* Click "Next"
* For this example deselect the "Logging" option
* Click "Next"
* Select your EC2 key Pair
* Under "Authentication" select your KerberosSecurityConfiguration
* Click "Create cluster"

### View status and terminate EMR cluster
You can view the status of your cluster or termiate the cluster by naviagting to >Services>EMR>Clusters within the AWS Console.

## Run an example Spark job on an EMR cluster

### Spark Job Description
You can submit Spark steps to a cluster as it is being created or to an already running cluster,

In this example we will execute a simple java function of a text file using Spark on EMR. This is a standard word count application that will return the distinct words in the file along with the count of the number of time the word is present.

The jar file containing the application will be stored and referenced in a S3 bucket along with the text file being analyzed. The results of the Spark job will be return to the same S3 bucket.

### Creating the S3 bucket

```bash
aws s3 mb s3://test-analysis-bucket --region us-east-2
```
### Copy files to S3
Clone the following file to a local folder:
https://github.com/cloudmesh-community/fa18-516-22/tree/master/chapter/applications

You can then sync the folder you stored the jar in to your S3 bucket folder.

```bash
aws s3 sync your-local-folder-path s3://test-analysis-bucket/SparkTutorial
```
Store a text file locally and use the S3 sync function to make it availaable in your S3 bucket.

```bash
aws s3 sync your-local-folder-path s3://test-analysis-bucket/SparkTutorial/Input
```

### Execute the Spark job on a running cluster
Using your cluster id and the paths within your S3 bucket run the following command (this assumes you have a cluster up and running).

```bash
aws emr add-steps --cluster-id your-cluster-id \
--steps Type=Spark,Name=”Spark Program”,ActionOnFailure=CONTINUE, \
Args=[ — class,test.spark.job.SparkJob, \
s3://test-analysis-bucket/SparkTutorial/SparkJob-1.0-SNAPSHOT.jar, \
s3://test-analysis-bucket/SparkTutorial/Input/input.txt, \
s3://test-analysis-bucket/SparkTutorial/Output]
```
### Execute the Spark job while creating clusters
We can also run the same Spark step during the creation of a cluster using the following command (assumes you have already done pre-steps to creating an EMR cluster).

In this case the EMR cluster will spin up, run the Spark job, persist the results to your S3 bucket, and then auto terminate.

```bash
aws emr create-cluster --name "Test-Kerberized-Spark-Cluster" \
--release-label emr-5.17.0 \
--instance-type m4.large \
--instance-count 3 \
--use-default-roles \
--ec2-attributes KeyName=your-key,SubnetId=your-subnet-id \
--security-configuration KerberosSecurityConfiguration \
--applications Name=Spark \
--kerberos-attributes Realm=EC2.INTERNAL,KdcAdminPassword=your-password \
--steps Type=Spark,Name="Spark Program",ActionOnFailure=CONTINUE, \
Args=[--class,test.spark.job.SparkJob, \
s3://test-analysis-bucket/SparkTutorial/SparkJob-1.0-SNAPSHOT.jar, \
s3://test-analysis-bucket/SparkTutorial/Input/input.txt, \
s3://test-analysis-bucket/SparkTutorial/Output] \
--auto-terminate
```
### View the results of the Spark job
You can use the AWS Console to view the results of the Spark Job.

Go to the AWS Console (ensure that the URL references your default region)

https://us-east-2.console.aws.amazon.com/elasticmapreduce/home?region=us-east-2#

Navigate to the S3 bucket and folder you specified for the output.

## Conclusion
AWS EMR is a powerful tool for distributive processing. It is easy to use from wither the command line utilizing AWS CLI or through the AWS Console web interface.

