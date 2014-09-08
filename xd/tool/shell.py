import sys
import os
import subprocess

import logging
log = logging.getLogger(__name__)


def chdir(path, quiet=False):
    """Change the current working directory to the specified path.

    Arguments:
    path -- absolute or relative path (relative to current working directory)
    quiet -- True: be quiet, False: print out notice about new working directory
    """
    log.debug("chdir: %s", path)
    try:
        cwd = os.getcwd()
    except OSError as e:
        cwd = None
    if (cwd and
        os.path.realpath(os.path.normpath(path)) == os.path.normpath(cwd)):
        return
    if not quiet:
        print('> cd', path)
    os.chdir(path)
    return


def call(cmd, path=None, quiet=False, success_returncode=0):
    """Run shell command.

    Arguments:
    cmd -- the command (with arguments), string or list
    path -- directory to use as working directory while running command
    quiet -- True: be quiet, False: print out command and output from it
    success_returncode -- command returncode to consider as success
    """
    log.debug("call: %s", cmd)

    if path:
        if not os.path.exists(path):
            return None
    else:
        path = ""

    # Git seems to have a problem with long paths __and__ generates
    # long relative paths when run from a symlinked path.  To
    # workaround this, we always switch to realpath before running any
    # commands.
    rpath = os.path.realpath(path)

    pwd = os.getcwd()
    chdir(rpath, quiet=True)

    if not quiet:
        if path:
            print('%s> %s'%(path, cmd))
        else:
            print('> %s'%(cmd))

    retval = None
    if quiet:
        process = subprocess.Popen(cmd, shell=isinstance(cmd, str),
                                   stdin=sys.stdin,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        output = process.communicate()[0]
        if process.returncode == success_returncode:
            retval = output

    else:
        returncode = subprocess.call(cmd, shell=isinstance(cmd, str),
                                     stdin=sys.stdin)
        if returncode == success_returncode:
            retval = True

    chdir(pwd, quiet=True)

    return retval
