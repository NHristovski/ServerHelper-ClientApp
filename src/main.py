import asyncio

from src.common import config_reader
from src.commands.command_listener import CommandListener


""" python -m src.main """


def main():
    loop = asyncio.get_event_loop()
    command_listener = CommandListener("nikola")

    try:
        command_listener.start_listening(config_reader.get_address(), config_reader.get_port())

        loop.run_forever()
    finally:
        command_listener.stop_listening("nikola")
        loop.close()


if __name__ == "__main__":
    main()
