import boto3
from .structs import DynamoItem


def get_dynamodb_client(region_name: str = "us-east-1") -> 'boto3.client':
    """
    Creates and returns a client object for interacting with AWS DynamoDB.

    This function initializes a DynamoDB client using the boto3 library, allowing for interactions with DynamoDB services within the specified AWS region.

    Parameters:
    - region_name (str, optional): The AWS region where the DynamoDB service is located. Defaults to 'us-east-1'.

    Returns:
    - boto3.client: A DynamoDB client object configured for the specified region.

    Example Usage:
    >>> dynamodb_client = get_dynamodb_client(region_name="us-west-2")
    """
    return boto3.client("dynamodb", region_name=region_name)


def put_item(dynamodb_client, table_name: str, item: DynamoItem):
    """
    Inserts an item into a specified DynamoDB table.

    This function utilizes an AWS DynamoDB client to insert an item into a specified table.
    The item to be inserted should be an instance of structs.DynamoItem or similar, 
    which must implement a to_dynamo_style method to convert the item into the format expected by DynamoDB.

    Parameters:
    - dynamodb_client: The DynamoDB client object to interact with the database. This client 
      should be obtained using the boto3 library.
    - table_name (str): The name of the DynamoDB table where the item will be inserted.
    - item (pyaws.DynamoItem): An instance of pyaws.DynamoItem or a similar object that represents 
      the item to be inserted. Must implement a to_dynamo_style() method.

    Returns:
    - dict: A dictionary representing the response from the DynamoDB put_item operation, 
      which includes information about the operation's result.

    Example:
    ```python
    # Assuming dynamodb_client is already created and configured
    item = DynamoItem(attribute1="value1", attribute2="value2")
    response = put_item(dynamodb_client, "my_table_name", item)
    ```
    """
    return dynamodb_client.put_item(
        TableName=table_name,
        Item=item.to_dynamo_style()
    )
