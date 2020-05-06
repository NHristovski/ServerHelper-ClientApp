import paho.mqtt.client as mqtt
import time
from src.common import config_reader


""" python -m src.common.publisher """


def on_connect(client, user_data, flags, rc):
    print("Connection returned with result code:", rc)


client = mqtt.Client("id_publisher")
client.on_connect = on_connect

client.connect(config_reader.get_address(), 1883, 60)

# for i in range(1,3000000):
#     print("iteration", i)
#     time.sleep(5)
#     payload = """{
#             "command_id": 1,
#             "command_type": "start",
#             "body": "echo test"
#         }"""
#     client.publish("nikola", payload=payload)

payload = """{
            "command_id": 10,
            "command_type": "start",
            "body": "echo a & echo b & ping -n 20 127.0.0.1 & echo c"
        }"""
client.publish("nikola", payload=payload)

print("start sent")

time.sleep(15)

payload = """{
            "command_id": 10,
            "command_type": "stop",
            "body": ""
        }"""
client.publish("nikola", payload=payload)

print("stop sent")

# client.loop_forever()
