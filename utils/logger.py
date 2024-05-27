import logging
import os
from gunicorn.glogging import Logger
from pythonjsonlogger import jsonlogger
from configs import config


"""
Hardcode the logging level here,
but it'd be better if handle the logging level on config.
"""


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Console Logging
    console_handler = logging.StreamHandler()

    # File Logging
    log_file_path = os.path.join(os.getcwd(), config.LOG_FILE)
    file_handler = logging.FileHandler(log_file_path)

    # Log Format
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add Logger Handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Setup Flask Logger
logger = setup_logger('flask-app')


# Gunicorn Logger
class GunicornJsonLogger(Logger):
    def setup(self, cfg):
        self.error_log = setup_logger('gunicorn-error')
        self.access_log = setup_logger('gunicorn-access')
        self.error_log.propagate = False
        self.access_log.propagate = False
