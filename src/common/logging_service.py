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


class LoggingService(metaclass=Singleton):
    def __init__(self):
        self.client = None
        self.topic =  "logs"

    def info(self, message: str):
        self.send_message("INFO", message)

    def warn(self, message: str):
        self.send_message("WARN", message)

    def error(self, message: str):
        self.send_message("ERROR", message)

    def send_message(self, type: str, message: str):
        if (self.client is None):
            self.create_client()

        user_id = config_reader.get_user_id()
        client_id = client_information.get_client_id()

        payload = f"""[ {datetime.utcnow()} ] [ {type} ] [ {user_id}:{client_id} ] {message} """

        self.client.publish(self.topic, payload)


    def create_client(self):
        self.client = mqtt.Client()

        self.client.on_connect = on_connect_closure()
        self.client.on_disconnect = on_disconnect_closure()
        self.client.on_message = on_message

        self.client.connect(host=config_reader.get_address(), port=config_reader.get_port(), keepalive=60)
