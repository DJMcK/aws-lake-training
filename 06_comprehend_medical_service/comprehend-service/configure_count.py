import json
import boto3
import time
import urllib
import os
import pandas as pd

s3 = boto3.resource('s3')

def handler(event, context):
    if event:
        # get the chunk size for comprehend calls from the environment variables
        comprehend_chunksize = os.environ['comprehend_chunksize']
        bucket_name = os.environ['bucket_name']
        file_keyname = event['data_node']['query_results']['results_file']

        # read the csv and convert to a pandas dataframe
        data = pd.read_csv(read_file_from_s3(bucket_name, file_keyname))
        print("^^^^ dataframe length")
        totalItemsToComprehend = len(data)
        print(len(data))
        
        # setup counts
        iterator = {}
        iterator['totalItemsToComprehend'] = totalItemsToComprehend
        iterator['comprehend_chunksize'] = int(comprehend_chunksize)
        iterator['comprehendedItems'] = 0
        iterator['iteration_num'] = 0

    return iterator

def read_file_from_s3(bucket_name, key):
    print(">> reading S3 object...")
    response = s3.Object(bucket_name, key).get()
    return response['Body']    