import json
import paho.mqtt.client as mqtt
from command_handler import CommandHandler


def on_connect_closure(topic):
    # Define the callback to handle CONNACK from the broker, if the connection created normal, the value of rc is 0
    def on_connect(client, userdata, flags, rc):
        # TODO logging service
        # logging_service.info("Connect: Result code:" + str(rc))
        # logging_service.warn("Connect: Result code:" + str(rc))
        # logging_service.error("Connect: Result code:" + str(rc))
        # TODO if rc not 0 then error
        client.subscribe(topic)
        print("Connect: Result code:" + str(rc))

    return on_connect


# Define the callback to hande publish from broker, here we simply print out the topic and payload of the received message
def on_message(client, userdata, msg):
    # print("Received message, topic:" + msg.topic + "payload:" + str(msg.payload))
    print(f'on message called with recieved msg: {msg.payload.decode("utf-8")}')
    cmd_attrb = json.loads(msg.payload.decode('utf-8'))

    cmdHandler = CommandHandler()
    cmdHandler.run_command(cmd_attrb)


def on_disconnect_closure(update_client):
    # Callback handles disconnection, print the rc value
    def on_disconnect(client: mqtt.Client, userdata, rc):
        print("Disconnetct: Connection returned result:" + str(rc))
        # update_client()

    return on_disconnect

class CommandListener:
    def __init__(self, topic):
        self.is_listening = False
        self.client = None
        self.topic = topic

    def start_listening(self, host, port):
        # TODO remove host and port as params , use consul to get host and port
        if not self.is_listening:
            print('will create client')
            self.is_listening = True
            self.create_client(host, port)
            self.client.loop_start()
        else:
            print('ERROR NO')
            # TODO send error log
            raise ValueError('Client is already listening!')

    def stop_listening(self, topic):
        if self.is_listening:
            self.is_listening = False
            self.client.unsubscribe(self.topic)
            self.client.loop_stop(force=True)
        else:
            # TODO send error log
            raise ValueError('Client is already stopped!')

    def create_client(self, host, port):
        self.client = mqtt.Client()

        self.client.on_connect = on_connect_closure(self.topic)
        self.client.on_disconnect = on_disconnect_closure(self.update_client)
        self.client.on_message = on_message

        # Connect to broker
        # connect() is blocking, it returns when the connection is successful or failed.
        # If you want client connects in a non-blocking way, you may use connect_async() instead
        # TODO use loop start
        self.client.connect_async(host=host, port=port, keepalive=60)

    def update_client(self, client):
        self.is_listening = False
        self.start_listening("0.0.0.0","0") # TODO change this
