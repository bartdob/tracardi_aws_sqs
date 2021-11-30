from pydantic import validator, create_model, AnyHttpUrl
from pydantic.main import BaseModel
from tracardi.domain.entity import Entity


class SqsAuth(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str


class Content(BaseModel):
    content: str
    type: str

    @validator('content')
    def must_have_2_letters(cls, v):
        print(v)
        if len(v) < 2:
            raise ValueError('String is too short. String must be at least two letters long.')
        return v


class AwsSqsConfiguration(BaseModel):
    source: Entity
    message: Content
    region_name: str
    queue_url: AnyHttpUrl
    delay_seconds: int
    message_attributes: str
