import paho.mqtt.client as mqtt
from src.commands.command_handler import CommandHandler
from src.common.models import CommandMessageJSON


command_handler: CommandHandler = CommandHandler()


def on_connect_closure(topic):
    def on_connect(client, user_data, flags, rc):
        # TODO logging service
        # logging_service.info("Connect: Result code:" + str(rc))
        # logging_service.warn("Connect: Result code:" + str(rc))
        # logging_service.error("Connect: Result code:" + str(rc))
        # TODO if rc not 0 then error
        client.subscribe(topic)
        print("Connect: Result code:", rc)

    return on_connect


def on_message(client, user_data, msg):
    command_message = CommandMessageJSON.from_json(msg.payload)

    command_handler.run_command(command_message)


def on_disconnect_closure(update_client):
    def on_disconnect(client: mqtt.Client, user_data, rc):
        print("Disconnect: Connection returned result:", rc)
        # update_client()

    return on_disconnect


class CommandListener:
    def __init__(self, topic):
        self.is_listening = False
        self.client = None
        self.topic = topic

    def start_listening(self, host, port):
        # TODO remove host and port as params, use consul to get host and port
        if not self.is_listening:
            print("will create client")
            self.is_listening = True
            self.create_client(host, port)
            self.client.loop_start()
        else:
            print("ERROR NO")
            # TODO send error log
            raise ValueError("Client is already listening!")

    def stop_listening(self, topic):
        if self.is_listening:
            self.is_listening = False
            self.client.unsubscribe(self.topic)
            self.client.loop_stop(force=True)
        else:
            # TODO send error log
            raise ValueError("Client is already stopped!")

    def create_client(self, host, port):
        self.client = mqtt.Client()

        self.client.on_connect = on_connect_closure(self.topic)
        self.client.on_disconnect = on_disconnect_closure(self.update_client)
        self.client.on_message = on_message

        self.client.connect_async(host=host, port=port, keepalive=60)

    def update_client(self, client):
        self.is_listening = False
        self.start_listening("0.0.0.0", "0")  # TODO change this