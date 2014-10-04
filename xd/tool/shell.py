import sys
import os
import subprocess

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def call(cmd, ok_code=[0]):
    """Run shell command.

    Run the given shell command, echoing command line to stdout, and
    just letting the output go to stdout and stderr.

    Arguments:
    cmd -- the command (with arguments), string or list
    ok_code -- command exit codes to consider as success
    """
    log.debug("call: %s", cmd)
    print('> %s'%(cmd))
    retval = None
    exit_code = subprocess.call(cmd, shell=isinstance(cmd, str),
                                stdin=sys.stdin)
    return exit_code in ok_code
