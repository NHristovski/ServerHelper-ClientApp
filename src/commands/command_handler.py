from typing import Dict

from src.commands.command_output_sender import CommandOutputSender
from src.commands.command_runner import CommandRunner
from src.common.logging_service import LoggingService
from src.common.models import CommandResultDTO, CommandFinalResult, CommandLineOutput, CommandMessageJSON, CommandType
from src.common.singleton import Singleton


logger: LoggingService = LoggingService()
command_output_sender: CommandOutputSender = CommandOutputSender()


def handle_result(result: CommandFinalResult):
    to_send = CommandResultDTO.from_result(result)
    command_output_sender.send_output(to_send)
    print("result >>>", result)


def handle_line(line: CommandLineOutput):
    to_send = CommandResultDTO.from_line(line)
    command_output_sender.send_output(to_send)
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
            if command_id in self.active_commands:
                runner = self.active_commands[command_id]
                runner.kill()
                del self.active_commands[command_id]
            else:
                logger.error(f"No command with id {command_id} is running.")
                raise ValueError(f"No command with id {command_id} is running.")
