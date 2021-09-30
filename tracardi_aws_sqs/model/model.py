from pydantic import validator
from pydantic.main import BaseModel
from tracardi.domain.entity import Entity


class SqsUrl(BaseModel):
    queueUrl: str


class SqsQueue(BaseModel):
    message: str


class AwsSqsConfiguration(BaseModel):
    source: Entity
    message: SqsQueue

    @validator('message')
    def myst_have_2_letter(cls, v):
        if len(v) < 2:
            raise ValueError('String is too short. String must be at least two letters long.')
        return v








