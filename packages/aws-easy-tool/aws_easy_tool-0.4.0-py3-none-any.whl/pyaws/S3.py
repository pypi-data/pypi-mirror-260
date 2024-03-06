import boto3
from typing import Dict, Any


def get_s3_client(region_name: str = "us-east-1"):
    return boto3.client("s3", region_name=region_name)


def put_item_from_local_path(
    s3_client,
    bucket_name: str,
    file_pth: str,
    s3_pth: str,
    extra_args: Dict[Any, Any] = {}
):
    response = s3_client.upload_file(
        Bucket=bucket_name,
        Filename=file_pth,
        Key=s3_pth,
        ExtraArgs=extra_args
    )

    return response


def get_item_from_s3(s3_client, bucket_name: str, s3_pth: str, local_file_pth: str) -> None:
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=s3_pth,
    )

    with open(local_file_pth, "wb") as F:
        F.write(response['Body'].read())
