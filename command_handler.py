from typing import Dict

from command_runner import CommandRunner,CommandFinalResult,CommandLineOutput


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def handle_result(result: CommandFinalResult):
    # """{
    #    "result_code" : 0
    #    "final" : True
    # }"""
    # TODO send result code to topic /output/command_id/
    print('command result> ', result)


def handle_line(line: CommandLineOutput):
    # """{
    #    "line" : "something"
    #    "final" : False
    # }"""
    # TODO send line to topic /output/command_id/
    print('command output> ', line)


class CommandHandler(metaclass=Singleton):
    def __init__(self):
        self.active_commands: Dict[int, CommandRunner] = {}
        pass

    def run_command(self, command: dict):
        command_id = command["command_id"]

        if command["command_type"] == "start":
            # print(f'CMD handler is starting command {command["body"]}')
            runner = CommandRunner(command_id, command["body"], handle_line, handle_result)
            runner.run()
            self.active_commands[command_id] = runner

        elif command["command_type"] == "stop":

            runner = self.active_commands[command_id]
            runner.kill()
            del self.active_commands[command_id]
