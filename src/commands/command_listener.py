import paho.mqtt.client as mqtt

from src.commands.command_handler import CommandHandler
from src.common.logging_service import LoggingService
from src.common.models import CommandMessageJSON
from src.common.mqtt_client_factory import MQttClientBuilder
from src.common.topic_getter import Topics

command_handler: CommandHandler = CommandHandler()
logger: LoggingService = LoggingService()


def on_connect_closure(topic):
    def on_connect(client, user_data, flags, rc):
        if rc == 0:
            client.subscribe(topic)
            logger.info("MQTT Connect Success! Result code: " + str(rc))
        else:
            logger.error("MQTT Connect Failed! Result code: " + str(rc))

    return on_connect


def on_message(client, user_data, msg):
    command_message = CommandMessageJSON.from_json(msg.payload)

    command_handler.run_command(command_message)


def on_disconnect(client: mqtt.Client, user_data, rc):
    if rc == 0:
        logger.info("MQTT Disconnect Success! Result code: " + str(rc))
    else:
        logger.error("MQTT Disconnect Failed! Result code: " + str(rc))


class CommandListener:
    def __init__(self):
        self.is_listening = False
        self.client = None
        self.topic = Topics.commands_topic()

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.create_client()
            self.client.loop_start()
            logger.info("Started listening for commands")
        else:
            logger.warn("Client is already listening!")
            raise ValueError("Client is already listening!")

    def stop_listening(self):
        if self.is_listening:
            self.is_listening = False
            self.client.unsubscribe(self.topic)
            self.client.loop_stop(force=True)
            logger.info("Stopped listening for commands")
        else:
            logger.warn("Client is already stopped!")
            raise ValueError("Client is already stopped!")

    def create_client(self):
        self.client = (MQttClientBuilder()
                       .on_connect(on_connect_closure(self.topic))
                       .on_message(on_message)
                       .on_disconnect(on_disconnect)
                       .async_connection()
                       .build_and_connect())
