# import paho.mqtt.client as mqtt
# import time

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))

# client = mqtt.Client("client_id_publisher")
# client.on_connect = on_connect

# client.connect("192.168.1.224", 1883, 60)

# for i in range(1,30):
#     time.sleep(3)
#     client.publish("nikola", "current itteration: " + str(i))

# client.loop()


# Import paho-mqtt Client class:
import paho.mqtt.client as mqtt
import time

# Define the callback to handle CONNACK from the broker, if the connection created normal, the value of rc is 0
def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))

# Define the callback to hande publish from broker, here we simply print out the topic and payload of the received message

# Create an instance of `Client`
client = mqtt.Client('id_publisher')
client.on_connect = on_connect

# Connect to broker
# connect() is blocking, it returns when the connection is successful or failed. If you want client connects in a non-blocking way, you may use connect_async() instead
client.connect("192.168.1.224", 1883, 60)


# for i in range(1,3000000):
#     print('testing')
#     time.sleep(5)
#     payload = """{
#             "command_id": 1,
#             "command_type": "start",
#             "body": "echo test"
#         }"""
#     client.publish("nikola", payload=payload)

# payload = """{
#             "command_id": 5,
#             "command_type": "start",    
#             "body": "echo test"
#         }"""
# client.publish("nikola", payload=payload)
payload = """{
            "command_id": 10,
            "command_type": "start",
            "body": "echo a & echo b & ping -n 20 127.0.0.1 & echo c"
        }"""
client.publish("nikola", payload=payload)

print('start sent')

time.sleep(5)

payload = """{
            "command_id": 10,
            "command_type": "stop",
            "body": ""
        }"""
client.publish("nikola", payload=payload)

print('stop sent')

client.loop_forever()

