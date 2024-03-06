# Python Imports
import logging
import os

# Django Imports

# Third-Party Imports

# Project-Specific Imports

# Relative Import


def get_logger(name):
    """This function creates a logger object with the given name and sets the logging level to INFO.
    It also adds a file handler to the logger which will log messages to the 'logs/clm.log' file.
    The formatter is set to include the time, name, level, filename, line number, function name and message in the log output.

    Args:
        name (str): Name of the logger.

    Returns:
        Logger: Logger object.
    """
    # Check if the 'logs' directory exists, create it if not
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Define the log file path
    log_file_path = os.path.join(logs_dir, 'microservice_utils.log')

    # Create the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if the log file exists, create it if not
    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()

    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

