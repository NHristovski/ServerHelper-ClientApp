from typing import Dict
from src.commands.command_runner import CommandRunner
from src.common.models import CommandResultDTO, CommandFinalResult, CommandLineOutput, CommandMessageJSON, CommandType
from src.common.singleton import Singleton


def handle_result(result: CommandFinalResult):
    to_send = CommandResultDTO.from_result(result)
    # TODO send result code to topic /output/command_id/
    print("result >>>", result)


def handle_line(line: CommandLineOutput):
    to_send = CommandResultDTO.from_line(line)
    # TODO send line to topic /output/command_id/
    print("line ->", line)


class CommandHandler(metaclass=Singleton):
    def __init__(self):
        self.active_commands: Dict[int, CommandRunner] = {}

    def run_command(self, command: CommandMessageJSON):
        command_id = command.command_id

        if command.command_type == CommandType.start:
            runner = CommandRunner(command_id, command.body, handle_line, handle_result)
            runner.run()
            self.active_commands[command_id] = runner
        elif command.command_type == CommandType.stop:
            runner = self.active_commands[command_id]
            runner.kill()
            del self.active_commands[command_id]
