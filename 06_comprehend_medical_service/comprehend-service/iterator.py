import json
import time
import urllib
import os

import logging
logger = logging.getLogger()
log_handler = logger.handlers[0]
log_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s:%(name)s:%(message)s", "%Y-%m-%d %H:%M:%S"))
logger.setLevel(logging.INFO)

def handler(event, context):
    if event:
        totalItemsToComprehend = event['iterator']['totalItemsToComprehend']
        comprehend_chunksize = event['iterator']['comprehend_chunksize']
        comprehendedItems = event['iterator']['comprehendedItems']

        # log the variables
        logger.info(">> INSIDE ITERATOR >>")
        logger.info(">> totalItemsToComprehend: {}".format(totalItemsToComprehend))
        logger.info(">> comprehend_chunksize: {}".format(comprehend_chunksize))
        logger.info(">> comprehendedItems: {}".format(comprehendedItems))


        # update the totalItemsToComprehend variable to reflect the number of items already comprehended 
        if (comprehendedItems < totalItemsToComprehend):     
            event['iterator']['continue_iterating'] = True
        else:
            event['iterator']['continue_iterating'] = False

        return event['iterator']