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
            # print('Putting messages on the queue')
            result = await client.send_message(QueueUrl=self.aws_config.queueUrl,
                                               MessageBody=self.aws_config.message)

        return Result(port="payload", value={
            "status": result.status,
            "body": await result.json()
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
            init={}
        ),
        metadata=MetaData(
            name='tracardi-aws-sqs',
            desc='plugin to send a message to a Amazon AWS SQS queue',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["Connectors"]
        )
    )