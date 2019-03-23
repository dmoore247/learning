import json
import iris
import requests
import urllib
import boto3
import os
from datetime import datetime
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def partition():
    now = datetime.utcnow() 
    return "/".join([str(now.year), str(now.month), str(now.day)])

def target_bucket():
    return os.environ['TARGET_BUCKET']

def parse_event(event):
    return (event['Message']['bucket'],event['Message']['key'])

region_url = "https://s3.eu-west-2.amazonaws.com"
def get_url(bucket, key):
    return '/'.join([region_url, bucket, key])

def download(url, key):
    urllib.request.urlretrieve(url, key) # save in this directory with same name
    return key

def parse(filename):
    return iris.load(filename)
    
def write(encoded_string, bucket, key):
    s3 = boto3.resource("s3")
    return s3.Bucket(bucket).put_object(Key=key, Body=encoded_string)

def cleanup():
    # remove temp files
    return

def lambda_handler(event, context):
    # TODO implement
    print('got event{}'.format(parse_event(event)))

    bucket, key = parse_event(event)
    url = get_url(bucket, key)
    key = download(url, key)
    [obj] = parse(key)
    encoded_string = str(obj).encode('utf-8')

    target = target_bucket()
    part = partition()
    path = "/".join([part, key + '.txt'])
    write(encoded_string, target, path)
    
    return {
        'statusCode': 200,
        'body': json.dumps( event )
    }


if __name__ == "__main__":
    print('starting')
    print ('done')
