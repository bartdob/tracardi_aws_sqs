import json
from asyncio.log import logger
import boto3

AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=

def send_message():
    sqs_client = boto3.client("sqs", region_name="eu-central-1")

    message = {"key": "value"}
    response = sqs_client.send_message(
        QueueUrl="https://sqs.eu-central-1.amazonaws.com/521597733500/MyQ",
        MessageBody=json.dumps(message)
    )
    print(response)


send_message()
