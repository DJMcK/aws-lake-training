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
athena = boto3.client('athena')

# setup configuration
S3_OUTPUT = 's3://jr-comprehend/athenaoutput'   # TODO replace bucket name
DATABASE = 'djm'
RETRY_COUNT = 10

# query all indications from last 2 years
query_all_indications = 'SELECT id, indications_and_usage FROM "djm"."djm_curated" where year >= \'2017\' and year <= \'2019\''

def handler(event, context):
    if event:
        logger.info(">> querying athena database")
        data_node = {}
        data_node['bucket_name'] = os.environ['bucket_name']

        # run query on athena
        response = athena.start_query_execution(
            QueryString = query_all_indications,
            QueryExecutionContext = {
                'Database': DATABASE
            },
            ResultConfiguration = {
                'OutputLocation': S3_OUTPUT,
                'EncryptionConfiguration': {
                    'EncryptionOption': 'SSE_S3'
                }
            }
        )
        query_execution_id = response['QueryExecutionId']
        logger.info(query_execution_id)

        # poll the query execution status to check if the query has completed execution
        for i in range(1, 1 + RETRY_COUNT):
            query_status = athena.get_query_execution(QueryExecutionId = query_execution_id)
            query_execution_status = query_status['QueryExecution']['Status']['State']

            if query_execution_status == 'SUCCEEDED':
                logger.info("STATUS:" + query_execution_status)
                break
            if query_execution_status == 'FAILED':
                logger.info(query_status)
                raise Exception("STATUS:" + query_execution_status)
            else:
                logger.info("STATUS:" + query_execution_status)
                time.sleep(5)
        else:
            athena.stop_query_execution(QueryExecutionId = query_execution_id)
            raise Exception('TIME OVER')

        result = athena.get_query_results(QueryExecutionId = query_execution_id)
        logger.info(result)

        # athena store the result of the query in the athena output bucket we had specified earlier. 
        # send the url of the athena result file to the next lambda function in the step function
        results_file = "athenaoutput/" + query_execution_id + '.csv'

        query_results = {}
        query_results['results_file'] = results_file
        query_results['query_execution_id'] = query_execution_id

        return query_results
