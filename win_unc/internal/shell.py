from subprocess import Popen, PIPE

from win_unc.errors import ShellCommandError
from win_unc.internal.loggers import no_logging


RETURN_CODE_SUCCESS = 0


def run(command, logger=no_logging):
    """
    Executes `command` in the shell and returns `stdout` and `stderr` as a tuple in that order.

    `logger` may be a function that takes a string for custom logging purposes. It defaults to a
    no-op.
    """
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    while process.poll() is None:
        try:
            # Write new lines in case the command prompts the us for some input.
            process.stdin.write('\n'.encode('utf-8'))
        except IOError:
            pass

    stdout, stderr = process.stdout.read().decode('utf-8'), process.stderr.read().decode('utf-8')
    if process.returncode == RETURN_CODE_SUCCESS:
        return stdout, stderr
    else:
        raise ShellCommandError(command, process.returncode)
