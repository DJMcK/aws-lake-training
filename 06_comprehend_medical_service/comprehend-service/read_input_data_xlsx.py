import json
import boto3
import time
import urllib
import pandas as pd

s3 = boto3.resource('s3')


def handler(event, context):
    if event:
        print('>> event: ' + json.dumps(event))
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_keyname = event['Records'][0]['s3']['object']['key']

        print('>> bucket_name: ' + bucket_name)
        print('>> file_keyname: ' + file_keyname)

        data = pd.read_excel(read_file_from_s3(bucket_name, file_keyname))
        print('>> data: ' + data)

    return True

def read_file_from_s3(bucket_name, key):
    print(">> reading S3 object...")
    response = s3.Object(bucket_name, key).get()
    return response['Body']
