import enum
import json
import sys
from dataclasses import dataclass
from datetime import datetime

from src.common.mqtt_client_factory import MQttClientBuilder
from src.common.topic_getter import Topics

""" python -m src.common.logs_subscriber """


def on_message_login(client, userdata, msg):
    print(f"[{datetime.now()}] {msg.topic}: {msg.payload}")
    response = json.loads(msg.payload)
    topic = Topics.response_login_topic(response["user_id"], response["client_id"])
    to_send = "success"
    client.publish(topic, to_send)
    print(f"sent {to_send} to {topic}")


def on_message_metrics(client, userdata, msg):
    print(f"[{datetime.now()}] {msg.topic}: {msg.payload[:10]}")


def on_message_logs(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))


@dataclass
class Subscription:
    topic: str
    message_handler: object


class SubscribeTo(enum.Enum):
    metrics = Subscription(Topics.response_metrics_topic(), on_message_metrics)
    login = Subscription(Topics.login_topic(), on_message_login)
    logs = Subscription(Topics.response_logs_topic(), on_message_logs)
    commands = Subscription(Topics.commands_output_topic(), on_message_logs)

    @classmethod
    def has(cls, item):
        return any(s.name == item for s in SubscribeTo)


def on_connect_closure(subscribe_to: SubscribeTo):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        client.subscribe(subscribe_to.topic)

    return on_connect


if len(sys.argv) <= 1:
    print("OH COME ON")
    exit()

subscription = sys.argv[1]
message_handler = None

if SubscribeTo.has(subscription):
    subscription = SubscribeTo[subscription].value
    message_handler = subscription.message_handler
else:
    print("OH COME ON")
    exit()

client = (MQttClientBuilder()
          .on_connect(on_connect_closure(subscription))
          .on_message(message_handler)
          .build_and_connect())

client.loop_forever()
