import os
from contextlib import contextmanager

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

__all__ = ['pushd']

@contextmanager
def pushd(path):
    """Temporary change current working directory.

    Current working directory will be changed to path, and restored back to
    the original value when leaving the context.

    Arguments:
    path -- absolute or relative path (relative to current working directory)
    """
    cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(cwd)
