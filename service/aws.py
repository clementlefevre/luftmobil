import socket
import time
import os
import json
import boto3
import logging

logger = logging.getLogger(__name__)


from service.converter import float_to_decimal,fill_empty_values

REMOTE_SERVER = "www.google.com"
def is_connected():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(REMOTE_SERVER)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        logger.info("CONNECTED !!!")
        return True
    except:
        logger.info("NOT CONNECTED ........")
    
    
    return False

def upload_data():
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('luftmobil')
    with open('data.json') as f:
        data = json.load(f)

    data = [float_to_decimal(d) for d in data]

    ## youpi ! AWS Dynamo cannot handle empty string.
    data = fill_empty_values(data)
    
    with table.batch_writer() as batch:
        for d in data:
          batch.put_item(d)
    os.remove("data.json")
