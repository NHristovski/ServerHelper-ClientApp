import asyncio

from src.common import config_reader
from src.commands.command_listener import CommandListener
from src.metrics.metrics_scheduler import MetricsScheduler


""" python -m src.main """


def main():
    loop = asyncio.get_event_loop()
    command_listener = CommandListener("nikola")
    metrics = MetricsScheduler()
    # TODO: somehow, send client_information.get_client_id() with config_read.get_user_id() to group 8

    try:
        metrics.start()
        command_listener.start_listening(config_reader.get_address(), config_reader.get_port())

        loop.run_forever()
    finally:
        print("Ended gracefully")
        command_listener.stop_listening("nikola")
        metrics.stop()
        loop.close()


if __name__ == "__main__":
    main()
