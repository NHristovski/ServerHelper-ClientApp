from src.common.models import CommandResultDTO
from src.common.singleton import Singleton
from src.common import config_reader
from src.common import client_information
import paho.mqtt.client as mqtt
from datetime import datetime


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

        user_id = config_reader.get_user_id()
        client_id = client_information.get_client_id()

        topic = f"/command_output/{user_id}/{client_id}/"

        payload = message.to_json()

        self.client.publish(topic, payload)

    def create_client(self):
        self.client = mqtt.Client()

        self.client.on_connect = on_connect_closure()
        self.client.on_disconnect = on_disconnect_closure()
        self.client.on_message = on_message

        self.client.connect(host=config_reader.get_address(), port=config_reader.get_port(), keepalive=60)
