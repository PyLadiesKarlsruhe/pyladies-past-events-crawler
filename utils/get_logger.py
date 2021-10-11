"""
Set up and customize the logger for the project
"""
import logging


def get_logger() -> logging.Logger:
    """
    Configures the root logger.
    :return: The root logger.
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(module)s: %(message)s',
        datefmt='%d.%m.%Y %H:%M:%S',
        level=logging.INFO
    )
    logger: logging.Logger = logging.getLogger()
    return logger
