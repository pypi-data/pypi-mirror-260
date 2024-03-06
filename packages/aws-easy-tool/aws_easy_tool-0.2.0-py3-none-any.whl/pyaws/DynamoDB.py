import boto3
from . import structs


def get_dynamodb_client():
    return boto3.client("dynamodb")


def put_item(dynamodb_client, table_name: str, item: structs.DynamoItem):
    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item.to_dynamo_style()
    )

    return response
