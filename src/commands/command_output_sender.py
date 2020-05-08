import paho.mqtt.client as mqtt

from src.common import config_reader
from src.common.models import CommandResultDTO
from src.common.mqtt_client_factory import MQttClientFactory
from src.common.singleton import Singleton
from src.common.topic_getter import Topics


def on_connect_closure():
    def on_connect(client, user_data, flags, rc):
        if rc == 0:
            print('LoggingService MQTT Connect Success')
        else:
            print('LoggingService MQTT Connect Failure!')

    return on_connect


# it will never be called
def on_message(client, user_data, msg):
    pass


def on_disconnect_closure():
    def on_disconnect(client: mqtt.Client, user_data, rc):
        print("Disconnect: Connection returned result:", rc)

    return on_disconnect


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
        self.client = MQttClientFactory.create(on_connect_closure(), on_message,
                                               config_reader.get_username(), config_reader.get_password(),
                                               config_reader.get_address(), config_reader.get_port(), keepalive=60,
                                               on_disconnect=on_disconnect_closure())
