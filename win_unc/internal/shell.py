import subprocess

from win_unc.internal.loggers import no_logging


class ShellCommandError(Exception):
    def __init__(self, command=None, error_code=None):
        self.command = command
        self.error_code = error_code

    def __str__(self):
        if self.command and self.error_code:
            return 'The command `{command}` exited with error code {code}.'.format(
                command=self.command, code=self.error_code)
        elif self.command:
            return 'The command `{command}` exited with an error.'.format(command=self.command)
        elif self.error_code:
            return 'Command exited with error code {code}.'.format(code=self.error_code)
        else:
            return 'Command exited with an error.'


def run(command, logger=no_logging):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout, stderr
    else:
        raise ShellCommandError(command, process.returncode)
