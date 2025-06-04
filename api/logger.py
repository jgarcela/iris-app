# logger.py
import logging
import sys
import os

# Solo creamos el logger si no existe
logger = logging.getLogger("web")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler("api/logs/api.log")
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - [API] - %(message)s'))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - [API] - %(message)s'))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
