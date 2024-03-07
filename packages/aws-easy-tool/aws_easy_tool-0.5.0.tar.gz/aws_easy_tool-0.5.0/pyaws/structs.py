from pydantic import BaseModel
from typing import Dict, Any
import uuid


class DynamoItem(BaseModel):
    def to_dynamo_style(self) -> Dict[str, Dict[str, Any]]:
        """
        Converts the model instance into a dictionary format compatible with DynamoDB.

        This method iterates through all the attributes of the model instance, converting
        them into a format that DynamoDB expects for its items. Specifically, it transforms
        each attribute into a dictionary with a type descriptor and the attribute value.
        Supported types are strings and numeric types (int, float), which are converted to
        DynamoDB's 'S' and 'N' types, respectively.

        Returns:
        - Dict[str, Dict[str, Any]]: A dictionary where each key corresponds to an attribute
          name, and the value is another dictionary specifying the type of the attribute ('S'
          for string, 'N' for numeric) and the attribute value itself.

        Raises:
        - ValueError: If an attribute is of an unsupported type, a ValueError is raised
          indicating the attribute name and its unsupported type.

        Example:
        Given an instance of `DynamoItem` with attributes `name: str` and `age: int`, calling
        `to_dynamo_style()` will return:
        ```python
        {
            "name": {"S": "John Doe"},
            "age": {"N": "30"}
        }
        ```

        Note: This method is specifically designed for use with AWS DynamoDB and expects
        that all model attributes can be categorized into string or numeric types. Other
        types (like lists or dictionaries) are not directly supported and would require
        additional handling.
        """
        dynamo_dict = {}

        for field_name, field_value in self.dict().items():
            if isinstance(field_value, str):
                dynamo_dict[field_name] = {"S": field_value}
            elif isinstance(field_value, (int, float)):
                dynamo_dict[field_name] = {"N": str(field_value)}
            else:
                raise ValueError(
                    f"Unsupported type for DynamoDB: {type(field_value)} for field '{field_name}'")

        return dynamo_dict


class SQSMessage(BaseModel):
    """
    A model for constructing messages to be sent to Amazon SQS.

    Attributes:
    - message_uuid (str): A unique identifier for the message, automatically generated
      using UUID4. This can be overridden if a specific UUID is required.
    - body (Dict[str, Any]): The content of the message. This is a dictionary that
      contains the actual data to be sent as the SQS message body.

    Example:
    To create a new SQS message with custom data:
    ```python
    message = SQSMessage(body={"key": "value"})
    ```

    This creates an `SQSMessage` instance with a unique `message_uuid` and a body
    containing the specified key-value pair.
    """

    message_uuid: str = str(uuid.uuid4())
    body: Dict[str, Any]
