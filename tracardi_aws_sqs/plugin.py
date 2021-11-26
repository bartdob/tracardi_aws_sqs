from tracardi.domain.resource import Resource
from tracardi.service.storage.driver import storage
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result
from tracardi_aws_sqs.model.model import AwsSqsConfiguration, SqsAuth
from aiobotocore.session import get_session


class AwsSqsAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'AwsSqsAction':
        config = AwsSqsConfiguration(**kwargs)
        source = await storage.driver.resource.load(config.source.id)
        return AwsSqsAction(config, source)

    def __init__(self, config: AwsSqsConfiguration, source: Resource):
        self.aws_config = config
        self.source = SqsAuth(**source.config)

    async def run(self, payload):
        session = get_session()
        async with session.create_client('sqs', region_name=self.aws_config.region_name,
                                         aws_secret_access_key=self.source.aws_secret_access_key,
                                         aws_access_key_id=self.source.aws_access_key_id
                                         ) as client:
            result = await client.send_message(QueueUrl=self.aws_config.queue_url,
                                               MessageBody=self.aws_config.message,
                                               DelaySeconds=self.aws_config.delay_seconds,
                                               MessageAttributes=self.aws_config.message_attributes)

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
            version='0.1',
            license="MIT",
            author="Bart Dobrosielski",
            init={
                "source": {
                    "id": None
                },
                "message": "",
                "region_name": "us-west-2",
                "queue_url": ""
            }
        ),
        metadata=MetaData(
            name='Simple queue service',
            desc='Plugin send a message to a Amazon AWS SQS queue',
            type='flowNode',
            width=200,
            height=100,
            icon='aws',
            tags=['aws'],
            group=["Amazon Web Services"]
        )
    )
