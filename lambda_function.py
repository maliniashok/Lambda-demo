import json
import boto3
import csv
import logging
from datetime import datetime, timedelta
# from random import randint
# from time import sleep
import time
# time.sleep(2 * 60)

# sleep(randint(2,4))

filename = "/tmp/" + str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".csv"
# current_time = datetime.now() + timedelta(minutes=5)
# print(current_time)
# required_time = datetime.now() - timedelta(minutes=5)
# print(required_time)


def cloudtrail_event():
    # s3 = boto3.client('s3')
    cloudtrail = boto3.client('cloudtrail')
    response = cloudtrail.lookup_events(
        LookupAttributes=[
        {
            'AttributeKey': 'EventName',
            'AttributeValue': 'CreateImage'
        }
        ],
        StartTime = datetime.now() - timedelta(minutes=10),
        EndTime = datetime.now() + timedelta(minutes=10)
    )
    print(response)
    test = response['Events']
    print(test)
    return test
    
def write_to_csv():
    print("Inside write_to_csv")
    time.sleep(4 * 60)
    image_output = cloudtrail_event()
    with open(str(filename), 'w') as csvfile:
        fieldnames=['EventSource', 'EventName', 'CloudTrailEvent', 'AccessKeyId', 'Resources', 'EventTime', 'ReadOnly', 'EventId', 'Username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for test in image_output:
            writer.writerow(test)

    return True
    
def upload_file(bucket='ssmbuckettest', region='us-east-1'):
    print("Inside upload_file")
    s3 = boto3.client('s3')
    if s3 is None:
        return None
    response = s3.upload_file(filename, bucket, filename)
    return True
    
def lambda_handler(event, context):
    if write_to_csv():
        print("Successfully wrote to csv file")
        upload_file('ssmbuckettest')
