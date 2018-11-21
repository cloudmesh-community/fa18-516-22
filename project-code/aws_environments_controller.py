import connexion
import six
import subprocess

from swagger_server import util


def create_emr():  # noqa: E501
    cluster_id=subprocess.run("aws emr create-cluster --name='MyJupyterHubCluster' --release-label emr-5.19.0 --applications Name=JupyterHub --log-uri s3://sims-analysis-bucket/MyJupyterClusterLogs --use-default-roles --instance-type m4.large --instance-count 2 --ec2-attributes KeyName=win-ec2-key")
    return cluster_id


def delete_emr(cluster_id):  # noqa: E501
    """Terminate EMR Cluster

     # noqa: E501

    :param cluster_id: 
    :type cluster_id: str

    :rtype: str
    """
    return 'do some magic!'


def get_status_emr(cluster_id):  # noqa: E501
    """Get the status of EMR cluster

     # noqa: E501

    :param cluster_id: 
    :type cluster_id: str

    :rtype: str
    """
    return 'do some magic!'
