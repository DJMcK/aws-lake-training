import json
import boto3
import time
import urllib
import os
import csv
import pandas as pd
import numpy as np

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
        comprehend_output_bucket_name = os.environ['comprehend_output_bucket_name']
        file_keyname = event['data_node']['query_results']['results_file']   
        print(">>> bucket name " + bucket_name)
        print(">>> comprehend output bucket name " + comprehend_output_bucket_name)
        print(">>> comprehend output file name " + file_keyname)
        results_file = event['data_node']['query_results']['results_file']
        # query_execution_id = event['data_node']['query_results']['query_execution_id']

        # read the iteration parameters from the event
        startIndex = event['iterator']['comprehendedItems']
        chunksize = event['iterator']['comprehend_chunksize']
        totalItemsToComprehend = event['iterator']['totalItemsToComprehend'] 
        iteration_num = event['iterator']['iteration_num'] 

        if ((startIndex + chunksize) <= totalItemsToComprehend):
            finalIndex = startIndex + chunksize
        else:
            finalIndex = totalItemsToComprehend
        
        # read the csv file into a dataframe and pull out a subset (startIndex - finalIndex)
        data = pd.read_csv(read_file_from_s3(bucket_name, file_keyname))         
        data_subset = data[startIndex:finalIndex]
        data_subset = data_subset.fillna('')


        # iterate through the pandas datframe subset and call comprehend medical
        data_to_persist = {}
        datalist = []
        for row in data_subset.itertuples():            
            dataitem = {}
            dataitem['id'] = row.id
            print(row.id)
            text_list = []
            # if indication_and_usage filed is empty -> replace the corresponding fields in the dataitem with NA.
            # also, we do not run the entity extraction on these empty texts
            temptext = row.indications_and_usage
            print(row.indications_and_usage)
            if temptext:
                result = client.detect_entities(Text = temptext)
                entities = result['Entities']
                for entity in entities:
                    text_list.append(entity['Text'])
                dataitem['extracted_text'] = text_list
            else:
                dataitem['indications_and_usage'] = 'NA'
                dataitem['extracted_entities'] = 'NA'
            datalist.append(dataitem)
        data_to_persist['datalist'] = datalist

        print("^^^^")
        print(data_to_persist['datalist'])
        # write out the enriched data to local lambda storage as a json
        with open('/tmp/comprehended.json', 'w') as outfile:
                json.dump(data_to_persist['datalist'], outfile)

        # setup the S3 url to write the comprehended data 
        comprehend_output = 'fda-product-indications/comprehendoutput/comprehended-' + str(iteration_num) + '.json'
        
        # write to s3 
        s3.meta.client.upload_file('/tmp/comprehended.json', Bucket = comprehend_output_bucket_name, Key = comprehend_output, ExtraArgs={'ServerSideEncryption':'AES256'})

        # do iteration housekeeping
        prev_comprehended_items = int(event['iterator']['comprehendedItems'])
        event['iterator']['comprehendedItems'] = len(data_subset) + prev_comprehended_items
        event['iterator']['iteration_num'] = iteration_num + 1

        # send the url of the written output file to the next lambda in the chain
        return event['iterator']     

def read_file_from_s3(bucket_name, key):
    print(">> reading S3 object...")
    response = s3.Object(bucket_name, key).get()
    return response['Body']      