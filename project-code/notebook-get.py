import boto3
import json
import subprocess

def search_nb_param_inpt_data(bucket, path, search_on):

    #call s3 API to get list of files including paths
    cmd = 'curl -X GET '
    cmd = cmd + 'http://ec2-18-191-50-79.us-east-2.compute.amazonaws.com:8081'
    cmd = cmd + '/api/s3?bucket=' + bucket + '&'
    cmd = cmd + 'path=' + path + '&extension=.ipynb'

    files = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    all_files = files.stdout.decode('utf-8')
    all_files = all_files.rstrip()

    return(all_files)
    
    s3 = boto3.resource('s3')
    
    #loop through all .ipynb under path
    nb_has_val = False
    nbs_found = []
    for file_path in all_files:

        content_object = s3.Object(bucket, file_path)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)

        #loop through each cell of nb
        for cell in json_content['cells']:
            if 'source' in cell:
                if 'metadata' in cell:
                    if 'tags' in cell['metadata']:
                        if 'parameters' in cell['metadata']['tags']:
                            if search_on in cell['source']:
                                nbs_found.append('s3://' + bucket + '/' + file_path)
                            
    rtn_nb_full_path_list = list(set(nbs_found))
    
    return(rtn_nb_full_path_list)
