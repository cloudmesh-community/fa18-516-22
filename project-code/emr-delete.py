import subprocess

def emr_delete(cid):

     subprocess.run("aws emr terminate-clusters --cluster-ids " + cid, shell=True)
     rtn_dict =   {
         "ClusterId": cid,
         "Status": "TERMINATING"
     }
     return rtn_dict
    
    
