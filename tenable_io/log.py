import logging as logging_
import sys

from tenable_io.config import TenableIOConfig


class LevelFilter(logging_.Filter):
    """ LevelFilter instances are used to filter messages by log level(s).
    """
    def __init__(self, levels):
        self.levels = levels if hasattr(levels, "__iter__") else []

    def filter(self, record):
        """ Log if returns non-zero, don't if returns zero.
        """
        return record.levelno in self.levels


LOGGER_NAME = 'tenable_io'
LOGGER_LEVEL = logging_.getLevelName(TenableIOConfig.get('logging_level'))
logging = logging_.Logger(LOGGER_NAME, LOGGER_LEVEL)


def configure_logging():
    # Create handler to log only `DEBUG` and `INFO` messages to stdout stream, and add to logger.
    stdout_handler = logging_.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging_.DEBUG)
    stdout_level_filter = LevelFilter([logging_.DEBUG, logging_.INFO])
    stdout_handler.addFilter(stdout_level_filter)
    logging.addHandler(stdout_handler)

    # Create handler to log levels greater than `INFO` to stderr stream, and add to logger.
    stderr_handler = logging_.StreamHandler()
    stderr_handler.setLevel(logging_.WARNING)
    logging.addHandler(stderr_handler)

    # Configure format of logged messages.
    formatter = logging_.Formatter(logging_.BASIC_FORMAT)
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

configure_logging()
