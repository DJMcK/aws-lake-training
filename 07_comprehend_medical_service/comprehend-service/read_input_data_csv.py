import json
import boto3
import time
import urllib
import os
import csv

import logging
logger = logging.getLogger()
log_handler = logger.handlers[0]
log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s", "%Y-%m-%d %H:%M:%S"))
logger.setLevel(logging.INFO)

s3 = boto3.resource('s3')

def handler(event, context):
    if event:
        print("read input data")
        bucket_name = event['data_node']['bucket_name']
        file_keyname = event['data_node']['file_keyname']

        response = s3.Object(bucket_name, file_keyname).get()

        #convert response to lines of CSV
        lines = response['Body'].read().decode('utf-8').split('\n')

        recordsList = []
        comprehend_request = {}

        for row in csv.DictReader(lines):
            print(json.loads(json.dumps(row)))
            recordsList.append(json.loads(json.dumps(row)))
            print("------")

        comprehend_request['records_list'] = recordsList
        return comprehend_request