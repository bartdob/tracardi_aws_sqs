from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_aws_sqs.plugin import AwsSqsAction

init = {
    "source": {
        "id": "aws"
    },
    "message": {"type": "application/json", "content": "{}"},
    "region_name": "us-west-2",
    "queue_url": "http://queue",
    "delay_seconds": "0",
    "message_attributes": "{}"
}
payload = {}
profile = Profile(id="profile-id")
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())
result = run_plugin(AwsSqsAction, init, payload,
                    profile)

print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
