import os
import shlex
import subprocess
import threading
import psutil
from typing import Optional, Callable, AnyStr, Tuple
from src.common.models import CommandFinalResult, CommandLineOutput, CommandStatus

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


def verify_and_clean_line(output: AnyStr) -> Tuple[bool, str]:
    def clean(line: str) -> str:
        clean_line = line.strip("\r\n")

        return clean_line

    def verify(clean_line: str) -> bool:
        return len(clean_line) > 0 and not clean_line.isspace()

    if isinstance(output, bytes):
        output = output.decode("utf-8")

    joined = os.linesep.join(filter(verify, map(clean, output.splitlines())))

    return verify(joined), joined


OnExitCallback = Optional[Callable[[CommandFinalResult], None]]
OnLineCallback = Optional[Callable[[CommandLineOutput], None]]


class CommandRunner:
    """ Wrapper class that utilizes subprocess.Popen and allows more control over processes
    Creates a process and runs it lazily (when .run() is called)
    Allows a function (on_exit) to be called on process end with the return code and output of the process
    Allows a function (on_line) to be called on each line output from the command
    Allows the process to be killed (using .kill()) with all sub-processes in the same group id
    At any time .is_complete() can be called to check if complete, and .output to get the output if complete
    Status available for each step in the lifecycle of a command
    """

    def __init__(self, command_id: int, command: str, on_line: OnLineCallback = None, on_exit: OnExitCallback = None):
        """ Creates a lazy CommandRunner which doesn't start the command until run is called
        :param command_id: command id which is part both output types
        :param command: the command that should be run, it must be a string
        :param on_line: optional callback function that is called for each line resulted on the output,
                        this is useful for long running processes when keeping track of output is essential
        :param on_exit: callback function that is called when the process ends,
                        it is called with the return code and the output of the process
                        note however that if on_line is supplied,
                        then the command string output of this line would be empty
        """

        if not isinstance(command, str):
            raise Exception("Command should be string")

        if len(command) <= 0:
            raise Exception("Command content can't be empty")

        self.__command_id = command_id
        self.__command: list = shlex.split(command)
        self.__on_line: OnLineCallback = on_line
        self.__on_exit: OnExitCallback = on_exit

        self.__process_id: Optional[int] = None
        self.__process: Optional[subprocess.Popen] = None
        self.__status: CommandStatus = CommandStatus.NotStarted
        self.__output: Optional[CommandFinalResult] = None

    @property
    def command_id(self):
        return self.__command_id

    @property
    def command(self):
        return self.__command

    @property
    def process_id(self):
        return self.__process_id

    @property
    def status(self):
        return self.__status

    @property
    def output(self):
        return self.__output

    @property
    def is_complete(self) -> bool:
        """ :return: whether the process completed (both successfully or killed) """

        return self.__status == CommandStatus.Killed or self.__status == CommandStatus.FinishedSuccessfully

    def run(self) -> threading.Thread:
        """ Runs the command in a separate thread
        While Running:
        - status is set to Running
        - on_line is called for each line output except empty lines
        When done:
        - status is set to FinishedSuccessfully
        - on_exit is called with the return code and std output
        :return: the thread where the process was running
        """

        def run_in_thread():
            process = subprocess.Popen(self.__command,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

            self.__status = CommandStatus.Running

            self.__process = process
            self.__process_id = process.pid

            if self.__on_line is not None:
                for line in process.stdout:
                    should_pass, clean_line = verify_and_clean_line(line)
                    if should_pass:
                        self.__on_line(CommandLineOutput(self.__command_id, clean_line))

            process.wait()

            output, _ = self.__process.communicate()

            self.__finish(output, CommandStatus.FinishedSuccessfully)

            return

        thread = threading.Thread(target=run_in_thread)
        thread.start()

        return thread

    def kill(self):
        """ Kills the process and each subprocess launched by the process
        Also sets status to Killed
        Still fills output with output of command and calls on_exit
        """

        if self.__status.Running and self.__process_id:
            # TODO: try: except NoSuchProcess: except AccessDenied:
            ps_util_process = psutil.Process(self.__process_id)

            # TODO: follow official guide https://psutil.readthedocs.io/en/latest/#kill-process-tree
            for descendent_process in ps_util_process.children(recursive=True):
                descendent_process.kill()

            ps_util_process.kill()

            self.__finish("", CommandStatus.Killed)
        else:
            raise ValueError("The process is not running!")

    def __finish(self, output: AnyStr, status: CommandStatus):
        return_code = self.__process.poll()

        should_pass, clean_line = verify_and_clean_line(output)

        self.__status = status
        self.__output = CommandFinalResult(self.__command_id, return_code, clean_line)

        if self.__on_exit is not None:
            self.__on_exit(self.__output)

    def __str__(self):
        return f"CommandRunner(id={self.command_id}, status={self.status}," \
               f" pid={self.__process_id}, command={self.command}"
