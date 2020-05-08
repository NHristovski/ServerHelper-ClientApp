import paho.mqtt.client as mqtt
from src.common import config_reader
from datetime import datetime


""" python -m src.common.logs_subscriber """


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("metrics_topic")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"[{datetime.now()}] {msg.topic}: {msg.payload[:10]}")
    # print(msg.topic + ": " + str(msg.payload))


client = mqtt.Client("client_id_listener")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=config_reader.get_username(), password=config_reader.get_password())
client.connect(config_reader.get_address(), config_reader.get_port(), 60)

client.loop_forever()
