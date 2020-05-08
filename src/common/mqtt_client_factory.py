import paho.mqtt.client as mqtt


class MQttClientFactory:
    @staticmethod
    def create(on_connect, on_message,
               username: str, password: str,
               host: str, port: int, keepalive: int, is_async=False,
               client_id: str = "",
               on_disconnect=None):
        client = mqtt.Client(client_id)
        client.on_connect = on_connect
        if on_disconnect:
            client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.username_pw_set(username=username, password=password)
        if is_async:
            client.connect_async(host, port, keepalive=keepalive)
        else:
            client.connect(host, port, keepalive=keepalive)

        return client
