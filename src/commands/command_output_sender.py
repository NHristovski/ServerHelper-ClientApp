import paho.mqtt.client as mqtt

from src.common.models import CommandResultDTO
from src.common.mqtt_client_factory import MQttClientBuilder
from src.common.singleton import Singleton
from src.common.topic_getter import Topics


def on_connect(client, user_data, flags, rc):
    if rc == 0:
        print('CommandOutputSender MQTT Connect Success')
    else:
        print('CommandOutputSender MQTT Connect Failure!')


# it will never be called
def on_message(client, user_data, msg):
    pass


def on_disconnect(client: mqtt.Client, user_data, rc):
    print("CommandOutputSender Disconnect: Connection returned result:", rc)


class CommandOutputSender(metaclass=Singleton):
    def __init__(self):
        self.client = None

    def send_output(self, message: CommandResultDTO):
        if self.client is None:
            self.create_client()

        if message.final and message.result_code is None:
            return

        topic = Topics.commands_output_topic()

        payload = message.to_json()

        self.client.publish(topic, payload)

    def create_client(self):
        self.client = (MQttClientBuilder()
                       .on_connect(on_connect)
                       .on_message(on_message)
                       .on_disconnect(on_disconnect)
                       .build_and_connect())
