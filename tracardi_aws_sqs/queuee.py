import json
from asyncio.log import logger
import boto3
import botocore
from dotenv import load_dotenv
import os
import asyncio
from aiobotocore.session import get_session
import sys

load_dotenv()  # take environment variables from .env.

user = 'bartSqs'

# def send_message1():
    # sqs_client = boto3.client("sqs",
    #                           region_name="eu-central-1",
    #                           aws_access_key_id=os.getenv('aws_ac_key_id'),
    #                           aws_secret_access_key=os.getenv('aws_sec_access_key')
    #                           )
    #
    # message = {"key": "hello Bart1"}
    # response = sqs_client.send_message(
    #     QueueUrl="https://sqs.eu-central-1.amazonaws.com/521597733500/MyQ",
    #     MessageBody=json.dumps(message)
    # )
    # print(response)
    # print(message)


async def send_message1():
        print("START")
        QUEUE_NAME = 'MyQ'
        msg_body = 'heeee'
        session = get_session()
        session = get_session()
        async with session.create_client('sqs', region_name='eu-central-1',
                                         aws_secret_access_key=os.getenv('aws_sec_access_key'),
                                         aws_access_key_id=os.getenv('aws_ac_key_id')
                                         ) as client:
            print('Putting messages on the queue')
            resp = await client.send_message(QueueUrl="https://sqs.eu-central-1.amazonaws.com/521597733500/MyQ",
                                             MessageBody=msg_body)
        print(resp)


def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_message1())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

