import asyncio
import time

import paho.mqtt.client as mqtt

from src.commands.command_listener import CommandListener
from src.common import config_reader, client_information
from src.common.logging_service import LoggingService
from src.common.mqtt_client_factory import MQttClientBuilder
from src.common.topic_getter import Topics
from src.metrics.metrics_scheduler import MetricsScheduler

""" python -m src.main """

logger: LoggingService = LoggingService()
connected = False
initial_seconds_to_sleep = 15  # * 60
seconds_to_sleep = initial_seconds_to_sleep


def on_connect(client: mqtt.Client, user_data, flags, rc):
    print("on_connect called")
    topic = Topics.response_login_topic()
    if rc == 0:
        logger.info("Login Client Connected Successfully To MQtt Broker")
        client.subscribe(topic)
        print(f"subscribed on {topic}")
        print("on_connect.rc=0")
    else:
        logger.error("Login Client Successfully Failed To Connect To MQtt Broker")
        print("on_connect.rc!=0")


def on_message(client: mqtt.Client, user_data, msg):
    print("on_message called")
    print("on_message.msg", msg)
    payload = msg.payload.decode('utf-8').lower()
    print("on_message.msg.payload", payload)
    global connected, seconds_to_sleep, initial_seconds_to_sleep

    if "success" in payload:
        connected = True
        print("on_message.success")
    elif "failure" in payload:
        seconds_to_sleep = initial_seconds_to_sleep
        print("54305732498-5723498057234980576439876-98746-07546089576589347 on_message.failed")
    else:
        print("this will never happen")


def send_login_request(client):
    # topic = f"/login/{config_reader.get_user_id()}/{client_information.get_client_id()}"
    payload = f"""
    {{
        "user_id": "{config_reader.get_user_id()}",
        "client_id": "{client_information.get_client_id()}"
    }}
    """
    topic = "/login"
    client.publish(topic, payload, qos=2)
    print("send_login_request.sent")


def start_working():
    loop = asyncio.get_event_loop()
    command_listener = CommandListener()
    metrics = MetricsScheduler()
    try:
        metrics.start()
        print('metrics')
        command_listener.start_listening()

        loop.run_forever()
        print('after run forever')
    finally:
        print("Ended gracefully")
        command_listener.stop_listening()
        metrics.stop()
        loop.close()


def main():
    global connected, seconds_to_sleep, initial_seconds_to_sleep

    client = (MQttClientBuilder()
              .on_connect(on_connect)
              .on_message(on_message)
              .async_connection()
              .build_and_connect())

    client.loop_start()

    while not connected:
        seconds_to_sleep = initial_seconds_to_sleep
        send_login_request(client)
        print(f"called send_login_request")
        print("goodnight")
        while not connected and seconds_to_sleep > 0:
            time.sleep(1)
            seconds_to_sleep -= 1
            # print(f"sleeping #{seconds_to_sleep}")

    print("HOORAY")
    start_working()


if __name__ == "__main__":
    main()
