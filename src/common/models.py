import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional, AnyStr


@dataclass
class CommandFinalResult:
    command_id: int
    return_code: int
    output: str
    killed: bool


@dataclass
class CommandLineOutput:
    command_id: int
    line: str


class CommandStatus(Enum):
    NotStarted = "NotStarted"
    Running = "Running"
    FinishedSuccessfully = "FinishedSuccessfully"
    Killed = "Killed"


@dataclass
class CommandResultDTO:
    command_id: int
    final: bool
    line_or_output: Optional[str] = None
    result_code: Optional[int] = None
    killed: Optional[bool] = None

    @classmethod
    def final(cls, command_id: int, result_code: int, output: Optional[str] = None, killed: Optional[bool] = False):
        return CommandResultDTO(command_id, final=True, result_code=result_code, line_or_output=output, killed=killed)

    @classmethod
    def line(cls, command_id: int, line: str):
        return CommandResultDTO(command_id, final=False, line_or_output=line)

    @classmethod
    def from_result(cls, result: CommandFinalResult):
        return cls.final(result.command_id, result.return_code, result.output, result.killed)

    @classmethod
    def from_line(cls, result: CommandLineOutput):
        return cls.line(result.command_id, result.line)

    def to_json(self):
        as_dict = {
            "command_id": self.command_id,
            "final": self.final
        }

        if self.final:
            as_dict["output"] = self.line_or_output
            as_dict["result_code"] = self.result_code
            as_dict["killed"] = self.killed
        else:
            as_dict["line"] = self.line_or_output

        return json.dumps(as_dict)


class CommandType(Enum):
    start = "start"
    stop = "stop"


@dataclass
class CommandMessageJSON:
    command_id: int
    command_type: CommandType
    body: Optional[str]

    @classmethod
    def from_json(cls, json_message: AnyStr):
        if isinstance(json_message, bytes):
            json_message = json_message.decode("utf-8")

        dictionary = json.loads(json_message)

        command_id_key = "command_id"
        command_type_key = "command_type"
        body_key = "body"

        required_keys = {command_id_key, command_type_key}

        if not required_keys <= dictionary.keys():
            raise Exception("command_id & command_type must be supplied in the JSON message")

        if not isinstance(dictionary[command_id_key], int):
            raise Exception("command_id not integer")

        if dictionary[command_type_key] not in ["start", "stop"]:
            raise Exception("command_type can either be start or stop only")

        if dictionary[command_type_key] == "start" and body_key not in dictionary:
            raise Exception("body must be supplied when command_type is start")

        if body_key not in dictionary:
            dictionary[body_key] = ""

        return CommandMessageJSON(dictionary[command_id_key],
                                  CommandType(dictionary[command_type_key]),
                                  dictionary[body_key])
