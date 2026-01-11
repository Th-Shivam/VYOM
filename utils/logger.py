import logging
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
LOG_LEVEL = env_vars.get("LOG_LEVEL", "INFO").upper()

# Define log level mapping
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# Set up logger
logger = logging.getLogger("VYOM")
logger.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handler to logger
if not logger.handlers:
    logger.addHandler(console_handler)

def get_logger(name: str = "VYOM"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(LOG_LEVELS.get(LOG_LEVEL, logging.INFO))
        logger.addHandler(console_handler)
    return logger
