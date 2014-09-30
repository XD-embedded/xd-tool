import contextlib
import os


@contextlib.contextmanager
def stdchannel_redirected(stdchannel, dest_filename=os.devnull):
    """
    A context manager to temporarily redirect stdout or stderr

    e.g.:

    with stdchannel_redirected(sys.stderr, os.devnull):
        ...
    """

    if not isinstance(stdchannel, int):
        stdchannel = stdchannel.fileno()

    try:
        oldstdchannel = os.dup(stdchannel)
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel)

        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel)
        if dest_file is not None:
            dest_file.close()
