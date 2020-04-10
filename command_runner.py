import os
import shlex
import subprocess
import threading
from dataclasses import dataclass
from sys import platform
from typing import Optional, Callable
import psutil

""" Observations:
subprocess.Popen allows launching commands and waiting for output
process = Popen([split command])
process.poll() returns exit code if complete or None if still running
process.wait() self-explanatory, optional param Timeout in seconds, else exception
process.communication() can take optional input, returns output and error output
                        (we are going to use this method on process complete to get output)
process.kill() | terminate() don't work in our case (will get back to this in a second)
Popen parameters:
shell: bool = False -> whether running a shell (like cmd)
                       we always put shell=True
                       otherwise we'll have to prefix the command with `cmd /c`
                       cmd /c is used to launch a cmd and execute the rest of the command in it
                       since most commands are not on os level but shell level 
stdin=None -> we'll use this if we want to communicate with the process
stdout=None -> we set it to subprocess.PIPE, but we can set it to other values too
stderr=None -> we set it to subprocess.STDOUT to merge with output
Below is a very early version of a wrapper around Popen to offer us more control and useful functionalities
"""


@dataclass
class CommandFinalResult:
    command_id: int
    return_code: int
    output: str


@dataclass
class CommandLineOutput:
    command_id: int
    line: str


OnExitCallback = Optional[Callable[[CommandFinalResult], None]]
OnLineCallback = Optional[Callable[[CommandLineOutput], None]]


class CommandRunner:
    """ Wrapper class that utilizes subprocess.Popen and allows more control over processes
    Creates a process and runs it lazily (when .run() is called)
    Allows a function (on_exit) to be called on process end with the return code and output of the process
    Allows the process to be killed (using .kill()) with all sub-processes in the same group id (FUTURE)
    At any time .is_complete() can be called to check if complete, and .output to get the output if complete
    Future:
        .was_killed() or .status which can be [not_started, running, killed, complete]
    """

    def __init__(self, command_id: int, command: str, on_line: OnLineCallback = None, on_exit: OnExitCallback = None):
        """ Creates a lazy CommandRunner which doesn't start the command until run is called
        :param command: the command that should be run, it must be a string
        :param on_exit: callback function that is called when the process ends,
                        it is called with the return code and the output of the process
        """

        # TODO: maybe multiple commands can be supplied and then after each one ends, the next one is run

        if type(command) is not str:
            raise Exception("Command should be string")
        if len(command) <= 0:
            raise Exception("Command content can't be empty")

        self.command_id = command_id
        self.command: list = shlex.split(command)
        self.on_exit: OnExitCallback = on_exit
        self.on_line: OnLineCallback = on_line
        self.__done: bool = False
        self.output: Optional[CommandFinalResult] = None
        self.process_id: Optional[int] = None

    def __set_done(self, return_code: int, output: str):
        self.__done = True
        self.__output = CommandFinalResult(self.command_id, return_code, output)

    def is_complete(self) -> bool:
        """ :return: whether the process completed """

        return self.__done

    def run(self) -> threading.Thread:
        """ Runs the command in a separate thread
        When done:
        - is_complete() returns true
        - on_exit is called with the return code and std output
        :return: the thread where the process was running
        """

        def run_in_thread():
            # print('run_in_thread called')
            process = subprocess.Popen(self.command,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

            self.process_id = process.pid

            if self.on_line is not None:
                for line in process.stdout:
                    # print('[[[ stdout line', line)
                    self.on_line(CommandLineOutput(self.command_id, line.strip().decode("utf-8")))

            process.wait()

            return_code = process.poll()
            output_bytes, _ = process.communicate()

            output = output_bytes.decode('utf-8')

            self.__set_done(return_code, output)

            if self.on_exit is not None:
                # print(']]] on_exit called')
                self.on_exit(CommandFinalResult(self.command_id, return_code, output))

            return

        thread = threading.Thread(target=run_in_thread)
        thread.start()

        return thread

    def kill(self):
        """ Missing
        :return:
        """

        if not self.is_complete() and self.process_id:
            psutil_process = psutil.Process(self.process_id)

            for proc in psutil_process.children(recursive=True):
                proc.kill()

            psutil_process.kill()
        else:
            raise ValueError('The process is not running!')
