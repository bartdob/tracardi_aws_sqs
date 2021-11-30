from tracardi_aws_sqs.model.model import MessageAttributes

attributes = MessageAttributes({
  "Title": "a",
  "Author": 1
})

print(attributes.dict())