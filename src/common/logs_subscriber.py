import paho.mqtt.client as mqtt
from src.common import config_reader


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("metrics_topic")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message recieved. The topic is " + msg.topic + ". The payload is: " + str(msg.payload))


client = mqtt.Client("client_id_listener")
client.on_connect = on_connect
client.on_message = on_message

client.connect(config_reader.get_address(), config_reader.get_port(), 60)

client.loop_forever()
