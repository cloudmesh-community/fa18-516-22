import subprocess

subprocess.run("aws emr terminate-clusters --cluster-ids " + cid, shell=True)
