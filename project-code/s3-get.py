import boto3

def search_s3_by_ext(bucket, path, extension):

    client = boto3.client('s3')
    obj = client.list_objects_v2(Bucket=mybucket, StartAfter=path )

    rtn_list = []
    for object in obj['Contents']:
        if object['Key'][-(len(file_extension)):] == file_extension:
            rtn_list.append(object['Key'])

    return(rtn_list)
