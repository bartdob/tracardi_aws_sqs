This plugin sends a message to amazon sqs queue

# Requirements

To use this plugin you must register at https://aws.amazon.com/sqs/ and obtain region_name - server located,
aws_secret_access_key and aws_access_key_id form amazon IAM

# Configuration

```json
{
  "region_name": "region_name for amazon sqs",
  "queueUrl": "url of the queue form amazon sqs",
  "aws_secret_access_key": "aws_secret_access_key form amazon IAM",
  "aws_access_key_id": "aws_access_key_id from amazon IAM",
  "message": "the message you put in to the queue"
}
```

# Input

This plugin does not take any input

# Output

Output returns status and response body form PushOver service. 

```json
{
  "status": 200,
  "body": {
    "status": 1,
    "result": "
    {'MD5OfMessageBody': '1888af887216fa96b34def217c4def61', 'MessageId': 'f173aa5f-0771-4299-8573-4bd2350da7c6', 
    'ResponseMetadata': {'RequestId': 'a74a21d7-989e-578f-90c4-780f26e1b68c', 'HTTPStatusCode': 200, 'HTTPHeaders': 
    {'x-amzn-requestid': 'a74a21d7-989e-578f-90c4-780f26e1b68c', 'date': 'Thu, 07 Oct 2021 09:22:07 GMT', 'content-type': 'text/xml', 'content-length': '378'}, 
    'RetryAttempts': 0}}"
  }
}