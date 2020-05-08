import json
import sys
from datetime import datetime

from src.common import config_reader
from src.common.mqtt_client_factory import MQttClientFactory
from src.common.topic_getter import Topics

""" python -m src.common.logs_subscriber """

to_subscribe_to = None


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    if to_subscribe_to == "metrics":
        client.subscribe(Topics.metrics_topic())
    elif to_subscribe_to == "login":
        client.subscribe(Topics.login_topic())
    elif to_subscribe_to == "logs":
        client.subscribe(Topics.logs_topic())
    elif to_subscribe_to == "commands":
        client.subscribe(Topics.commands_output_topic())


def on_message_login(client, userdata, msg):
    print(f"[{datetime.now()}] {msg.topic}: {msg.payload}")
    response = json.loads(msg.payload)
    topic = Topics.response_login_topic()
    to_send = "success"
    client.publish(topic, to_send)
    print(f"sent {to_send} to {topic}")


def on_message_metrics(client, userdata, msg):
    print(f"[{datetime.now()}] {msg.topic}: {msg.payload[:10]}")


def on_message_logs(client, userdata, msg):
    print(msg.topic + ": " + str(msg.payload))


if len(sys.argv) <= 1:
    print("OH COME ON")

# noinspection PyRedeclaration
to_subscribe_to = sys.argv[1]
message_handler = None
if to_subscribe_to == "metrics":
    message_handler = on_message_metrics
elif to_subscribe_to == "login":
    message_handler = on_message_login
elif to_subscribe_to == "logs":
    message_handler = on_message_logs
elif to_subscribe_to == "commands":
    message_handler = on_message_logs
else:
    print("OH COME ON")

client = MQttClientFactory.create(on_connect, message_handler,
                                  config_reader.get_username(), config_reader.get_password(),
                                  config_reader.get_address(), config_reader.get_port(), keepalive=60)

client.loop_forever()
