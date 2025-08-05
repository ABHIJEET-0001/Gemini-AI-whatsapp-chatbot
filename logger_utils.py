import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs folder if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Logger setup
logger = logging.getLogger('logtest')
logger.setLevel(logging.INFO)

# Formatter for logs
formatter = logging.Formatter(
    fmt='%(asctime)s pid/%(process)d [%(filename)s:%(lineno)d] %(message)s'
)

# File Handler
file_handler = RotatingFileHandler(
    filename='./logs/logtest.log',
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=10
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
