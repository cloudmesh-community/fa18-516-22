import subprocess

def emr_delete(cid):

     subprocess.run("aws emr terminate-clusters --cluster-ids " + cid, shell=True)
     rtn_dict =   {
         "ClusterId": cid,
         "Status": "TERMINATING"
         "CheckClusterStatus": ("http://ec2-18-191-50-79.us-east-2.compute.amazonaws.com:8080/api/emr/" + cid)
     }
     return rtn_dict
      
