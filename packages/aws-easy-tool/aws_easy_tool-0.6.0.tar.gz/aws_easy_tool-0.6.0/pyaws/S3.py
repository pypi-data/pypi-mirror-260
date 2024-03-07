import boto3
from typing import Dict, Any


def get_s3_client(region_name: str = "us-east-1"):
    """
    Creates and returns an Amazon S3 client configured for the specified region.

    This function simplifies the creation of an S3 client by encapsulating the boto3.client 
    call and setting the desired AWS region. The client can be used to interact with Amazon S3, 
    allowing for operations such as uploading, downloading, and listing objects within S3 buckets.

    Parameters:
    - region_name (str, optional): The AWS region to which the S3 client will be configured. 
      Defaults to "us-east-1".

    Returns:
    - boto3.client: An instance of a boto3 S3 client configured for the specified region.

    Example:
    ```python
    s3_client = get_s3_client(region_name="us-west-2")
    ```
    """
    return boto3.client("s3", region_name=region_name)


def put_item_from_local_path(
    s3_client,
    bucket_name: str,
    file_pth: str,
    s3_pth: str,
    extra_args: Dict[Any, Any] = {}
):
    """
    Uploads a file from a local path to an S3 bucket at the specified path.

    This function uses an Amazon S3 client to upload a file from the local filesystem
    to an S3 bucket. It allows for additional arguments to be specified, which can
    include options such as ACLs, ContentType, etc., as defined by the AWS S3 `upload_file` API.

    Parameters:
    - s3_client: The S3 client object to interact with Amazon S3. This client should be obtained
      using the boto3 library.
    - bucket_name (str): The name of the S3 bucket where the file will be uploaded.
    - file_pth (str): The path to the file on the local filesystem that is to be uploaded.
    - s3_pth (str): The key under which the file should be stored in the S3 bucket.
    - extra_args (Dict[Any, Any], optional): A dictionary of extra arguments that may be passed
      to the `upload_file` method. This can be used to set additional upload options such
      as metadata, content type, access control, etc.

    Returns:
    - The response from the S3 client's `upload_file` method. Typically, this function does not
      return anything unless there is an error during the upload process.

    Example:
    ```python
    # Assuming s3_client is already created and configured
    put_item_from_local_path(
        s3_client=s3_client,
        bucket_name='my-bucket',
        file_pth='/path/to/local/file.txt',
        s3_pth='folder/on/s3/file.txt',
        extra_args={'ACL': 'public-read', 'ContentType': 'text/plain'}
    )
    ```
    """
    return s3_client.upload_file(
        Bucket=bucket_name,
        Filename=file_pth,
        Key=s3_pth,
        ExtraArgs=extra_args
    )


def get_item_from_s3(s3_client, bucket_name: str, s3_pth: str, local_file_pth: str) -> None:
    """
    Downloads an item from an S3 bucket to a local file path.

    This function retrieves an object stored in an Amazon S3 bucket and saves it to
    a specified local file path. It utilizes an S3 client to fetch the object based on
    its bucket name and key. The object's content is then written to a local file,
    creating or overwriting the file at the specified path.

    Parameters:
    - s3_client: The S3 client object used for interacting with Amazon S3. This client
      should be obtained using the boto3 library.
    - bucket_name (str): The name of the S3 bucket from which the object will be downloaded.
    - s3_pth (str): The key of the object within the S3 bucket. This specifies the path of the
      object to be downloaded.
    - local_file_pth (str): The path on the local filesystem where the downloaded object will
      be saved. If the specified file exists, it will be overwritten.

    Returns:
    - None: This function does not return a value but raises exceptions on failure.

    Example:
    ```python
    # Assuming s3_client is already created and configured
    get_item_from_s3(
        s3_client=s3_client,
        bucket_name='my-bucket',
        s3_pth='folder/on/s3/file.txt',
        local_file_pth='/path/to/local/file.txt'
    )
    ```
    Note: Ensure that the AWS credentials used by `boto3` have the necessary permissions
    to access the specified S3 object and bucket.
    """
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=s3_pth,
    )

    with open(local_file_pth, "wb") as F:
        F.write(response['Body'].read())
