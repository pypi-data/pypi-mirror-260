from pydantic import BaseModel
from typing import Dict, Any
import uuid


class DynamoItem(BaseModel):
    def to_dynamo_style(self) -> Dict[str, Dict[str, Any]]:
        """
        TODO:
        """

        dynamo_dict = {}

        for field_name, field_value in self.dict().items():
            if isinstance(field_value, str):
                dynamo_dict[field_name] = {"S": field_value}
            elif isinstance(field_value, (int, float)):
                dynamo_dict[field_name] = {"N": str(field_value)}
            else:
                raise ValueError(f"Unsupported type for DynamoDB: {type(field_value)} for field '{field_name}")

        return dynamo_dict


class SQSMessage(BaseModel):
    message_uuid: str = str(uuid.uuid4)
    body: Dict[str, Any]
