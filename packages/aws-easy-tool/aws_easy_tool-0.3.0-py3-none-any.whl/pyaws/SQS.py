import boto3
import json
import uuid

from typing import Dict, List, Any
from .structs import SQSMessage


def get_sqs_client(region_name: str):
    return boto3.client("sqs", region_name=region_name)


def add_message_to_queue(
    sqs_client,
    output_queue_url: str,
    message: SQSMessage,
    message_group_id: str,
    message_deduplication_id: str = str(uuid.uuid4())
):
    response = sqs_client.send_message(
        QueueUrl=output_queue_url,
        MessageBody=json.dumps(dict(message)),
        MessageGroupId=message_group_id,
        MessageDeduplicationId=message_deduplication_id
    )

    return response


def read_from_queue(
    sqs_client,
    input_queue_url: str,
    max_number_of_messages: int = 1,
    message_attribute_names: List[str] = ['All'],
    wait_time_seconds: int = 0
):
    response = sqs_client.receive_message(
        QueueUrl=input_queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=max_number_of_messages,
        MessageAttributeNames=message_attribute_names,
        WaitTimeSeconds=wait_time_seconds
    )

    return response


def delete_from_queue(sqs_client, input_queue_url: str, receipt_handle: Dict[str, Any]):
    response = sqs_client.delete_message(
        QueueUrl=input_queue_url,
        ReceiptHandle=receipt_handle
    )
