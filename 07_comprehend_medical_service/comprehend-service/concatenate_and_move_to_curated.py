import json
import boto3
import time
import urllib
import pandas as pd
import os
import s3fs
from io import StringIO

s3 = boto3.resource('s3')

def handler(event, context):
    if event:
        print('>> inside concatenate_move_curated lambda function')
        landing_bucket_name = os.environ['comprehend_landing_bucket_name']
        curated_bucket_name = os.environ['comprehend_curated_bucket_name']
        bucket = s3.Bucket(landing_bucket_name)
        
        print(landing_bucket_name)
        print(curated_bucket_name)
        
        prefix_str = "fda-product-indications/comprehendoutput/"
        prefix_objs = bucket.objects.filter(Prefix=prefix_str)
        output_list = []
        print(prefix_objs)
        for obj in prefix_objs:
            print('>> {0}:{1}'.format(bucket.name, obj.key))
            obj = s3.Object(bucket.name, obj.key)
            data = obj.get()['Body'].read().decode('utf-8')
            output_list.append(json.loads(data))
 
        # write out the enriched data to local lambda storage as a json
        with open('/tmp/comprehended-final.json', 'w') as outfile:
                json.dump(output_list[0], outfile)

        # setup the S3 url to write the comprehended data 
        comprehend_output = 'fda-product-indications/comprehendoutput/comprehended-final.json'
        
        # write to s3 
        s3.meta.client.upload_file('/tmp/comprehended-final.json', Bucket = curated_bucket_name, Key = comprehend_output, ExtraArgs={'ServerSideEncryption':'AES256'})
