from pydantic import validator
from pydantic.main import BaseModel
from tracardi.domain.entity import Entity


class SqsAuth(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str


class SqsQueue(BaseModel):
    message: str


class AwsSqsConfiguration(BaseModel):
    source: Entity
    message: SqsQueue
    region_name: str
    queueUrl: str

    @validator('message')
    def must_have_2_letters(cls, v):
        if len(v) < 2:
            raise ValueError('String is too short. String must be at least two letters long.')
        return v








