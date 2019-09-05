import json
import boto3
import time
import urllib
import os

# import logging
# logger = logging.getLogger()
# log_handler = logger.handlers[0]
# log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s", "%Y-%m-%d %H:%M:%S"))
# logger.setLevel(logging.INFO)

def handler(event, context):
    if event:
        client = boto3.client('stepfunctions')
        print('>> inside proxy lambda')
        print('>> aws_request_id: ' + context.aws_request_id)
        print('>> environment variable: ' + os.environ['statemachine_arn'])
        statemachine = os.environ['statemachine_arn']

        # build a json object with the relevant data for the next stage
        data = {}
        data['data_node'] = {}
        data['data_node']['bucket_name'] = event['Records'][0]['s3']['bucket']['name']
        data['data_node']['file_keyname']  = event['Records'][0]['s3']['object']['key']
        # data['data_node']['aws_request_id'] = 'dqs-scrape-requests/' + context.aws_request_id
        client.start_execution(stateMachineArn = statemachine, input=json.dumps(data))



    