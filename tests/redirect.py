from contextlib import contextmanager
import os


@contextmanager
def stdout_redirected(dest_filename=os.devnull):
    """
    A context manager to temporarily redirect stdout

    e.g.:

    with stdout_redirected():
        ...

    Arguments:
    dest_filename -- filename/path to redirect to (default is os.devnull)
    """
    old_stdout = os.dup(1)
    try:
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), 1)
        yield
    finally:
        if old_stdout is not None:
            os.dup2(old_stdout, 1)
        if dest_file is not None:
            dest_file.close()

@contextmanager
def stderr_redirected(dest_filename=os.devnull):
    """
    A context manager to temporarily redirect stderr

    e.g.:

    with stderr_redirected():
        ...

    Arguments:
    dest_filename -- filename/path to redirect to (default is os.devnull)
    """
    old_stderr = os.dup(2)
    try:
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), 2)
        yield
    finally:
        if old_stderr is not None:
            os.dup2(old_stderr, 2)
        if dest_file is not None:
            dest_file.close()


@contextmanager
def stdchannels_redirected(dest_filename=os.devnull):
    """
    A context manager to temporarily redirect stdout and stderr

    e.g.:

    with output_redirected():
        ...
    """

    old_stdout = os.dup(1)
    old_stderr = os.dup(2)
    try:
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), 1)
        os.dup2(dest_file.fileno(), 2)
        yield
    finally:
        os.dup2(old_stdout, 1)
        os.dup2(old_stderr, 2)
        if dest_file is not None:
            dest_file.close()
