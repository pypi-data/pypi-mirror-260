# AWS SDK

A simple tool to perform daily tasks.

## How to Install

```
pip3 install aws-easy-tool
```

## Usage

### DynamoDB

Currently, we only support send an item to DynamoDB:

```[python]
import uuid
import pyaws
import time

class MyDynamoItem(pyaws.structs.DynamoItem):
    username: str
    password: str
    email: str
    uuid: str
    timestamp: int

my_item = MyDynamoItem(
    username="johndoe",
    password="123456",
    email="john@doe.com",
    uuid=str(uuid.uuid4()),
    timestamp=int(time.time() \* 1000)
)

dynamo_client = pyaws.DynamoDB.get_dynamodb_client()
response = pyaws.DynamoDB.put_item(dynamo_client, table_name="users", item=my_item)

# You can check, later, the HTTP response inside the `response` variable.
```

### Simple Storage Service (S3)

To get or put a file to S3, we assume that you'll upload a local file stored in your computer/server.

```[python]
import pyaws

s3_client = pyaws.SimpleStorageService.get_s3_client()

response = pyaws.SimpleStorageService.put_item_from_local_path(
    s3_client=s3_client,
    bucket_name="my-website",
    file_pth="/tmp/index.html",
    s3_pth="index.html" # -> It will store in the root of the bucket.
)

# You can check, later, the HTTP response inside the `response` variable.
```

### Simple Queue Service (SQS)

We assume that you have set your Queue as a First-In-First-Out (FIFO) queue in your AWS console.

```[python]

import pyaws

sqs_client = pyaws.SimpleQueueService.get_sqs_client()

# This is a simple template to follow to send your messages through the SQS queue.
# it has already a message uuid in case you want it.
message = pyaws.structs.SQSMessage(
    body={
        "message": "Hello World
    }
)

response = pyaws.SimpleQueueService.add_message_to_queue(
    sqs_client=sqs_client,
    output_queue_url="your-sqs-queue-url",
    message=message,
    message_group_id="my-message-group-id"
)
```
