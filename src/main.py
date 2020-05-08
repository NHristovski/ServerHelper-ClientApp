import asyncio

from src.common import config_reader
from src.commands.command_listener import CommandListener
from src.metrics.metrics_scheduler import MetricsScheduler


""" python -m src.main """


def main():
    loop = asyncio.get_event_loop()
    command_listener = CommandListener("nikola")
    metrics = MetricsScheduler()
    # TODO: try login every N minutes
    # maybe even with user input() (read on start not from config)
    # TODO: somehow, send client_information.get_client_id() with config_reader.get_user_id() to group 8
    # requests.post(config_reader.get_server_instance_management_url()/register, {client_id, user_id})
    # if http 200 then start listen else log error

    try:
        metrics.start()
        print('metrics')
        command_listener.start_listening(config_reader.get_address(), config_reader.get_port())

        loop.run_forever()
        print('after run forever')
    finally:
        print("Ended gracefully")
        command_listener.stop_listening("nikola")
        metrics.stop()
        loop.close()


if __name__ == "__main__":
    main()
