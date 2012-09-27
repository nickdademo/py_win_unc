"""
Contains functions for interacting with the shell easily.
"""

import subprocess

from win_unc.errors import ShellCommandError
from win_unc.internal.loggers import no_logging


RETURN_CODE_SUCCESS = 0


def run(command, logger=no_logging):
    """
    Executes `command` in the shell and returns `stdout` and `stderr` as a tuple in that order.

    `logger` may be a function that takes a string for custom logging purposes. It defaults to a
    no-op.
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == RETURN_CODE_SUCCESS:
        return stdout, stderr
    else:
        raise ShellCommandError(command, process.returncode)
