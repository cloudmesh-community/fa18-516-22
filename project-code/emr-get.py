import boto3

client = boto3.client('emr')
pdns = client.describe_cluster(ClusterId=cid)

rtn_dict =   {
     #"ClusterId": cid,
     #"CheckClusterStatus": ("http://ec2-18-191-50-79.us-east-2.compute.amazonaws.com:8081/emr/get/?" + cid),
     #"JupyterHub": ("https://" + response + ":9443"),
     "JupyterUN": "jovyan",
     "JupyterPW": "jupyter"
   }

response = client.list_clusters(ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING'])
