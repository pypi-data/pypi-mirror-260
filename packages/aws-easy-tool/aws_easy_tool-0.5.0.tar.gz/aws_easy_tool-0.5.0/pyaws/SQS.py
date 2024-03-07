import boto3
import json
import uuid

from typing import Dict, List, Any
from .structs import SQSMessage


def get_sqs_client(region_name: str = "us-east-1"):
    """
    Creates and returns an Amazon SQS client object configured for a specified region.

    This function simplifies the process of creating an SQS client with AWS Boto3, allowing
    for easy interaction with Amazon SQS services. The client can be used to send, receive,
    and delete messages, along with other SQS operations.

    Parameters:
    - region_name (str, optional): The name of the AWS region where the SQS service is located.
      The default value is "us-east-1".

    Returns:
    - boto3.client: An SQS client object configured for the specified AWS region. This client
      object can be used to interact with Amazon SQS.

    Example:
    ```python
    sqs_client = get_sqs_client(region_name="us-west-2")
    ```

    This example creates an SQS client for the "us-west-2" region. The returned client can be
    used for various SQS operations such as creating queues, sending messages to queues, receiving
    messages from queues, and deleting messages from queues.

    Note: To use this function, ensure that the AWS credentials are properly set up in your
    environment and that they have permissions to access Amazon SQS services.
    """
    return boto3.client("sqs", region_name=region_name)


def add_message_to_queue(
    sqs_client,
    output_queue_url: str,
    message: SQSMessage,
    message_group_id: str,
    message_deduplication_id: str = str(uuid.uuid4())
):
    """
    Sends a message to an Amazon SQS queue with support for message deduplication and grouping.

    This function is specifically designed for FIFO (First-In-First-Out) queues where both
    message deduplication and grouping are important concepts. It serializes the message into
    a JSON string and sends it to the specified SQS queue.

    Parameters:
    - sqs_client: The SQS client object used for interacting with Amazon SQS. This client
      should be obtained using the boto3 library.
    - output_queue_url (str): The URL of the SQS queue where the message will be sent.
    - message (SQSMessage): The message to be sent to the queue. This should be an instance
      of a class or a data structure that supports dictionary-like serialization.
    - message_group_id (str): The identifier of the message group. Amazon SQS uses this for
      grouping messages together. All messages with the same message group ID are processed
      in a FIFO manner.
    - message_deduplication_id (str, optional): The identifier for the message deduplication.
      This is used to ensure messages are not processed more than once. Defaults to a
      randomly generated UUID, making each message unique.

    Returns:
    - The response from the SQS `send_message` call, which includes details about the
      operation's result.

    Example:
    ```python
    # Assuming sqs_client is already created and configured
    message = {'key': 'value'}  # Example message
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue.fifo'
    message_group_id = 'my-message-group'
    response = add_message_to_queue(
        sqs_client=sqs_client,
        output_queue_url=queue_url,
        message=message,
        message_group_id=message_group_id
    )
    ```
    Note: This function is intended for use with FIFO queues. For standard queues, message
    grouping and deduplication IDs are not required.
    """
    return sqs_client.send_message(
        QueueUrl=output_queue_url,
        MessageBody=json.dumps(dict(message)),
        MessageGroupId=message_group_id,
        MessageDeduplicationId=message_deduplication_id
    )


def read_from_queue(
    sqs_client,
    input_queue_url: str,
    max_number_of_messages: int = 1,
    message_attribute_names: List[str] = ['All'],
    wait_time_seconds: int = 0
):
    """
    Retrieves messages from an Amazon SQS queue.

    This function fetches a specified number of messages from an SQS queue, with options to
    select specific message attributes and to use long polling for the message retrieval.

    Parameters:
    - sqs_client: The SQS client object used for interacting with Amazon SQS. This client
      should be obtained using the boto3 library.
    - input_queue_url (str): The URL of the SQS queue from which messages will be retrieved.
    - max_number_of_messages (int, optional): The maximum number of messages to retrieve
      in one call. The maximum value allowed by SQS is 10. Defaults to 1.
    - message_attribute_names (List[str], optional): The names of the message attributes
      to retrieve along with each message. Defaults to ['All'], indicating that all available
      attributes should be retrieved.
    - wait_time_seconds (int, optional): The duration (in seconds) for which the call will
      wait for a message to arrive in the queue before returning. A value of 0 disables
      long polling. The maximum value is 20 seconds. Defaults to 0.

    Returns:
    - dict: A dictionary representing the response from the SQS `receive_message` call,
      which may include one or more messages, depending on availability and the specified
      parameters.

    Example:
    ```python
    # Assuming sqs_client is already created and configured
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
    messages = read_from_queue(
        sqs_client=sqs_client,
        input_queue_url=queue_url,
        max_number_of_messages=5,
        wait_time_seconds=10
    )
    ```

    Note: If long polling is enabled by setting `wait_time_seconds` to a value greater than 0,
    the call may block for up to that duration or until a message becomes available.
    """
    return sqs_client.receive_message(
        QueueUrl=input_queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=max_number_of_messages,
        MessageAttributeNames=message_attribute_names,
        WaitTimeSeconds=wait_time_seconds
    )


def delete_from_queue(sqs_client, input_queue_url: str, receipt_handle: Dict[str, Any]):
    """
    Deletes a message from an Amazon SQS queue.

    This function removes a message from the queue specified by the input queue URL using
    the message's receipt handle. The receipt handle is a unique identifier for the message
    on the queue, provided by SQS when a message is received.

    Parameters:
    - sqs_client: The SQS client object used for interacting with Amazon SQS. This client
      should be obtained using the boto3 library.
    - input_queue_url (str): The URL of the SQS queue from which the message will be deleted.
    - receipt_handle (Dict[str, Any]): The receipt handle of the message to be deleted. This
      is typically obtained from the response of the `receive_message` call when messages
      are fetched from the queue.

    Returns:
    - dict: A dictionary representing the response from the SQS `delete_message` call, which
      includes information about the operation's result.

    Example:
    ```python
    # Assuming sqs_client is already created and configured, and a message has been received
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/my-queue'
    receipt_handle = received_message['Messages'][0]['ReceiptHandle']  # Example receipt handle
    response = delete_from_queue(
        sqs_client=sqs_client,
        input_queue_url=queue_url,
        receipt_handle=receipt_handle
    )
    ```

    Note: It's important to delete messages from the queue after processing to prevent them
    from being received and processed again. Messages not deleted will become visible again
    in the queue after the visibility timeout expires.
    """
    return sqs_client.delete_message(
        QueueUrl=input_queue_url,
        ReceiptHandle=receipt_handle
    )
