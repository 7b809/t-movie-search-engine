import logging
import sys

APP_NAME = "t_movie_search_engine"


def get_logger(name: str = APP_NAME) -> logging.Logger:
    """
    Console logger only.
    Logs are printed to terminal.
    No file logging.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.propagate = False

    return logger


logger = get_logger()
