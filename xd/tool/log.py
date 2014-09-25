import logging


class ConsoleFormatter(logging.Formatter):
    """A logging formatter for use when logging to console.

    Log message above logging.INFO will be prefixed with the levelname, fx.:

    ERROR: this is wrong

    And logging.DEBUG messages will be prefixed with name of the logger, which
    should normally be the module name, fx.:

    xd.tool.shell: chdir /home/user/my-project

    To achive this (logger name being the module name), all modules should
    setup logging this way:

    import logging
    log = logging.getLogger(__name__)
    """

    def __init__(self):
        """Initialize the formatter."""
        logging.Formatter.__init__(self)
        return

    def formatMessage(self, record):
        """Format the specified record message as text."""
        fmt = ""
        if record.levelno > logging.INFO:
            fmt += "%(levelname)s: "
        if record.levelno == logging.DEBUG:
            fmt += "%(name)s: "
        fmt += "%(message)s"
        return fmt % record.__dict__


def init(stream=None, level=logging.INFO):
    """Initialize logging module for logging to console.

    The root_logger will be setup and initialized to output print out
    logging.INFO (default) level and above.

    This function should only be called once.  Additional calls will be
    silently ignored.

    Arguments:
    stream -- stream to log to (sys.stderr if None)
    level -- minimum logging level to output (default is INFO)
    """
    if 'console_logger' in globals():
        return
    global console_logger
    root_logger = logging.getLogger()
    console_formatter = ConsoleFormatter()
    console_logger = logging.StreamHandler(stream=stream)
    console_logger.setFormatter(console_formatter)
    console_logger.setLevel(level)
    root_logger.addHandler(console_logger)


def deinit():
    """De-initialize logging module for logging to console."""
    if not 'console_logger' in globals():
        return
    global console_logger
    logging.getLogger().removeHandler(console_logger)
    del console_logger
