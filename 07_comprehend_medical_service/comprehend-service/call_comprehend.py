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
client = boto3.client(service_name='comprehendmedical', region_name='us-east-2')

def handler(event, context):
    if event:
        logger.info(">> calling comprehend medical to extract entities")
        
        # get the url of the athena results file from the event
        bucket_name = os.environ['bucket_name']
        results_file = event['data_node']['query_results']['results_file']
        query_execution_id = event['data_node']['query_results']['query_execution_id']

        # read the results file
        response = s3.Object(bucket_name, results_file).get()
        #convert response to lines of csv
        lines = response['Body'].read().decode('utf-8').split('\n')

        # convert each line of the csv to a json format
        recordsList = []
        for row in csv.DictReader(lines):
            logger.info(json.loads(json.dumps(row)))
            recordsList.append(json.loads(json.dumps(row)))
            print("------")

        data_to_persist = {}
        datalist = []

        for record in recordsList:
                dataitem = {}
                dataitem['id'] = record['id']
                # if indication_and_usage filed is empty -> replace the corresponding fields in the dataitem with NA.
                # also, we do not run the entity extraction on these empty texts
                temptext = record['indications_and_usage']
                if temptext:
                        dataitem['indications_and_usage'] = temptext
                        result = client.detect_entities(Text= record['indications_and_usage'])
                        entities = result['Entities']
                        for entity in entities:
                                print('Entity', entity)
                        dataitem['extracted_entities'] = result['Entities']
                else:
                        dataitem['indications_and_usage'] = 'NA'
                        dataitem['extracted_entities'] = 'NA'
                datalist.append(dataitem)
        data_to_persist['datalist'] = datalist

        # write out the enriched data to local lambda storage as a json
        with open('/tmp/comprehended.json', 'w') as outfile:
                json.dump(data_to_persist['datalist'], outfile)

        # setup the S3 url to write the enriched data. 
        comprehend_output = 'comprehendoutput/' + query_execution_id + '/comprehended.json'
        # write to s3 
        s3.meta.client.upload_file('/tmp/comprehended.json', Bucket=bucket_name, Key=comprehend_output, ExtraArgs={'ServerSideEncryption':'AES256'})
    # send the url of the written output file to the next lambda in the chain
    return comprehend_output        