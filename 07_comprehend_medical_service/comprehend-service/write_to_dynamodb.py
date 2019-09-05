import json
import boto3
import time
import urllib
import os

import logging
logger = logging.getLogger()
log_handler = logger.handlers[0]
log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s", "%Y-%m-%d %H:%M:%S"))
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    if event:
        logger.info(">> writing to dynamodb")
        table = dynamodb.Table('comprehendoutputtable')

        # get the url of the data to be written
        bucket_name = os.environ['bucket_name']
        comprehend_output = event['data_node']['comprehend_output']

        # get the url of the data to be written
        obj = s3.get_object(Bucket = bucket_name, Key = comprehend_output)
        data = obj['Body'].read().decode('utf-8')
        itemsList = json.loads(data)
        for element in itemsList:
            print("----->")
            print(element["id"])
            print(element["indications_and_usage"])
            print(element["extracted_entities"])
            
        # write the data as batch query into dynamodb
        with table.batch_writer() as batch:
                for item in itemsList:
                        # format the extracted items to a string
                        extracted_entities = item['extracted_entities']
                        eelist = []
                        
                        # if no entities are extracted, create a placeholder in the list. 
                        if not extracted_entities:
                                eelist = ['no entities extracted']

                        for entity in extracted_entities:
                                eelist.append(json.dumps(entity))
                        formatted_item = {
                                'textId': item['id'],
                                'indicationsText': item['indications_and_usage'],
                                'extractedEntities': ' || '.join(eelist)
                        }
                        batch.put_item(Item = formatted_item)


        