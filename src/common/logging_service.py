from datetime import datetime

import paho.mqtt.client as mqtt

from src.common import config_reader, client_information
from src.common.mqtt_client_factory import MQttClientBuilder
from src.common.singleton import Singleton
from src.common.topic_getter import Topics


def on_connect(client, user_data, flags, rc):
    if rc == 0:
        print('LoggingService MQTT Connect Success')
    else:
        print('LoggingService MQTT Connect Failure!')


# it will never be called
def on_message(client, user_data, msg):
    pass


def on_disconnect(client: mqtt.Client, user_data, rc):
    print("LoggingService Disconnect: Connection returned result:", rc)


class LoggingService(metaclass=Singleton):
    def __init__(self):
        self.client = None
        self.topic = Topics.logs_topic()

    def info(self, message: str):
        self.send_message("INFO", message)

    def warn(self, message: str):
        self.send_message("WARN", message)

    def error(self, message: str):
        self.send_message("ERROR", message)

    def send_message(self, type: str, message: str):
        if self.client is None:
            self.create_client()

        user_id = config_reader.get_user_id()
        client_id = client_information.get_client_id()

        payload = f"""[ {datetime.utcnow()} ] [ {type} ] [ {user_id}:{client_id} ] {message} """

        self.client.publish(self.topic, payload)

    def create_client(self):
        self.client = (MQttClientBuilder()
                       .on_connect(on_connect)
                       .on_message(on_message)
                       .on_disconnect(on_disconnect)
                       .build_and_connect())
