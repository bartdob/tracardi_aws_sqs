import json
from asyncio.log import logger
import boto3
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

user = 'bartSqs'

def send_message():
    sqs_client = boto3.client("sqs",
                              region_name="eu-central-1",
                              aws_access_key_id=os.getenv('aws_ac_key_id'),
                              aws_secret_access_key=os.getenv('aws_sec_access_key')
                              )

    message = {"key": "hello Bart1"}
    response = sqs_client.send_message(
        QueueUrl="https://sqs.eu-central-1.amazonaws.com/521597733500/MyQ",
        MessageBody=json.dumps(message)
    )
    print(response)
    print(message)


send_message()
