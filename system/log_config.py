import logging
import os
import sys
import datetime

from network import filesystem

from system import settings


def configure_logging(log_file_path: str) -> None:
    """configure the logging.

    Args:
        log_file_path (str): filepath for where to create the log files.
    """
    filesystem.init_directory(log_file_path)

    date_time = datetime.datetime.now().strftime(settings.LOG_DATE_TIME)
    log_file = os.path.join(log_file_path, f"log_{date_time}")

    _log_format = "%(asctime)s (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

    logging.basicConfig(filename=log_file, level=settings.LOG_LEVEL, format=_log_format)

    logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout))
