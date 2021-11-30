from pydantic import validator, create_model
from pydantic.main import BaseModel
from tracardi.domain.entity import Entity


class SqsAuth(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str


class AwsSqsConfiguration(BaseModel):
    source: Entity
    message: str
    region_name: str
    queue_url: str
    delay_seconds: int
    message_attributes: dict

    @validator('message')
    def must_have_2_letters(cls, v):
        print(v)
        if len(v) < 2:
            raise ValueError('String is too short. String must be at least two letters long.')
        return v








