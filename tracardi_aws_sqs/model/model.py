from pydantic import validator
from pydantic.main import BaseModel


class QueueMessage(BaseModel):
    message: str

    @validator('message')
    def myst_have_2_letter(cls, v):
        if len(v) < 2:
            raise ValueError('String is too short. String must be at least two letters long.')
        return v


class SqsQueue(BaseModel):
    message: QueueMessage
    queueUrl: str

class PushOverConfiguration(BaseModel):
    source: Entity
    message: str


