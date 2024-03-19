# log_config.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os

def configure_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)

    # define the directory for logs
    log_directory = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_path = os.path.join(log_directory, log_file)

    # Create a file handler
    handler = TimedRotatingFileHandler(log_path, when='midnight', backupCount=100)
    
    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger