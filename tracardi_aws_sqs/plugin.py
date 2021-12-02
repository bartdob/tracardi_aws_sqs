import json

from tracardi.domain.resource import ResourceCredentials
from tracardi.service.storage.driver import storage
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result
from tracardi_aws_sqs.model.model import AwsSqsConfiguration, SqsAuth, MessageAttributes
from aiobotocore.session import get_session
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent


def validate(config: dict):
    return AwsSqsConfiguration(**config)


class AwsSqsAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'AwsSqsAction':
        config = validate(kwargs)
        resource = await storage.driver.resource.load(config.source.id)
        return AwsSqsAction(config, resource.credentials)

    def __init__(self, config: AwsSqsConfiguration, credentials: ResourceCredentials):
        self.aws_config = config
        self.credentials = credentials.get_credentials(self, output=SqsAuth)  # type: SqsAuth

    async def run(self, payload):
        session = get_session()
        async with session.create_client('sqs', region_name=self.aws_config.region_name,
                                         aws_secret_access_key=self.credentials.aws_secret_access_key,
                                         aws_access_key_id=self.credentials.aws_access_key_id
                                         ) as client:

            if isinstance(self.aws_config.message_attributes, str) and len(self.aws_config.message_attributes):
                attributes = MessageAttributes(json.loads(self.aws_config.message_attributes))
                attributes = attributes.dict()
                result = await client.send_message(QueueUrl=self.aws_config.queue_url,
                                                   MessageBody=self.aws_config.message.content,
                                                   DelaySeconds=self.aws_config.delay_seconds,
                                                   MessageAttributes=attributes)
            else:
                result = await client.send_message(QueueUrl=self.aws_config.queue_url,
                                                   MessageBody=self.aws_config.message.content,
                                                   DelaySeconds=self.aws_config.delay_seconds)

            status_ok = result.get("ResponseMetadata", {}).get("HTTPStatusCode")  # response from server

            if status_ok in [200, 201, 202, 203, 204]:
                return Result(port="payload", value={
                    "status": status_ok,
                    "body": result
                }), Result(port="success", value={
                    "status": "success"})
            else:
                return Result(port="payload", value={
                    "status": status_ok,
                    "body": result
                }), Result(port="error", value={
                    "status": "error",
                    "body": status_ok
                })


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_aws_sqs.plugin',
            className='AwsSqsAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.6.0.1',
            license="MIT",
            author="Bart Dobrosielski",
            init={
                "source": {
                    "id": None
                },
                "message": {"type": "application/json", "content": "{}"},
                "region_name": "us-west-2",
                "queue_url": "",
                "delay_seconds": "0",
                "message_attributes": "{}"
            },
            form=Form(groups=[
                FormGroup(
                    name="SQS source",
                    fields=[
                        FormField(
                            id="source",
                            name="AWS SQS resource",
                            description="Select AWS SQS resource.",
                            required=True,
                            component=FormComponent(type="resource", props={"label": "resource"})
                        ),
                        FormField(
                            id="region_name",
                            name="AWS region",
                            description="Provide AWS region.",
                            component=FormComponent(type="select", props={"items": {'af-south-1',
                                                                                    'ap-east-1',
                                                                                    'ap-northeast-1',
                                                                                    'ap-northeast-2',
                                                                                    'ap-northeast-3',
                                                                                    'ap-south-1',
                                                                                    'ap-southeast-1',
                                                                                    'ap-southeast-2',
                                                                                    'ap-southeast-3',
                                                                                    'ca-central-1',
                                                                                    'eu-central-1',
                                                                                    'eu-north-1',
                                                                                    'eu-south-1',
                                                                                    'eu-west-1',
                                                                                    'eu-west-2',
                                                                                    'eu-west-3',
                                                                                    'me-south-1',
                                                                                    'sa-east-1',
                                                                                    'us-east-1',
                                                                                    'us-east-2',
                                                                                    'us-west-1',
                                                                                    'us-west-2'}})
                        ),
                        FormField(
                            id="queue_url",
                            name="AWS SQS url",
                            description="Provide AWS SQS url.",
                            component=FormComponent(type="text", props={"label": "url"})
                        ),
                    ]
                ),
                FormGroup(
                    name="SQS Message",
                    fields=[
                        FormField(
                            id="message",
                            name="Message",
                            description="Type message to be send. By selecting one of the tabs you define "
                                        "the request content-type.",
                            component=FormComponent(type="contentInput", props={"label": "Content", "rows": 6})
                        ),
                        FormField(
                            id="message_attributes",
                            name="Message attributes",
                            description="Type attributes to be send along with message.",
                            component=FormComponent(type="json", props={"label": "Attributes", "rows": 5})
                        ),
                        FormField(
                            id="delay_seconds",
                            name="Message delay",
                            component=FormComponent(type="text", props={"label": "Delay"})
                        )
                    ]
                ),
            ]),
        ),
        metadata=MetaData(
            name='Simple queue service',
            desc='Plugin that sends a message to the Amazon AWS SQS queue',
            type='flowNode',
            width=200,
            height=100,
            icon='aws',
            tags=['aws'],
            group=["Amazon Web Services"]
        )
    )
