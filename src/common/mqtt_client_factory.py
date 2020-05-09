from typing import Optional, Callable, Any

import paho.mqtt.client as mqtt

from src.common import config_reader

on_connect_type = Callable[[mqtt.Client, Any, Any, int], None]
on_message_type = Callable[[mqtt.Client, Any, mqtt.MQTTMessage], None]
on_disconnect_type = Callable[[mqtt.Client, Any, int], None]


class MQttClientBuilder:
    def __init__(self):
        self.__client_id: str = ""
        self.__on_connect: Optional[on_connect_type] = None
        self.__on_message: Optional[on_message_type] = None
        self.__on_disconnect: Optional[on_disconnect_type] = None
        self.__login_username: str = config_reader.get_username()
        self.__login_password: str = config_reader.get_password()
        self.__connect_is_async: bool = False
        self.__connect_address: str = config_reader.get_address()
        self.__connect_port: int = config_reader.get_port()
        self.__connect_keepalive: int = 60

    def client_id(self, client_id: str) -> 'MQttClientBuilder':
        self.__client_id = client_id
        return self

    def on_connect(self, on_connect: on_connect_type) -> 'MQttClientBuilder':
        self.__on_connect = on_connect
        return self

    def on_message(self, on_message: on_message_type) -> 'MQttClientBuilder':
        self.__on_message = on_message
        return self

    def on_disconnect(self, on_disconnect: on_disconnect_type) -> 'MQttClientBuilder':
        self.__on_disconnect = on_disconnect
        return self

    def login(self, username: str, password: str) -> 'MQttClientBuilder':
        self.__login_username = username
        self.__login_password = password
        return self

    def connection(self, address: str, port: int = 1883, keepalive: int = 60) -> 'MQttClientBuilder':
        self.__connect_address = address
        self.__connect_port = port
        self.__connect_keepalive = keepalive
        return self

    def async_connection(self, is_async: bool = True) -> 'MQttClientBuilder':
        self.__connect_is_async = is_async
        return self

    def build_and_connect(self) -> mqtt.Client:
        client = mqtt.Client(self.__client_id)

        if self.__on_connect:
            client.on_connect = self.__on_connect

        if self.__on_message:
            client.on_message = self.__on_message

        if self.__on_disconnect:
            client.on_disconnect = self.__on_disconnect

        client.username_pw_set(self.__login_username, self.__login_password)

        if self.__connect_is_async:
            client.connect_async(self.__connect_address, self.__connect_port, self.__connect_keepalive)
        else:
            client.connect(self.__connect_address, self.__connect_port, self.__connect_keepalive)

        return client
