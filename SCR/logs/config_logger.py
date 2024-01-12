#logs/config_logger.py
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

def configurar_logging():
    logger = logging.getLogger()
    if logger.hasHandlers():
        return logger

    # Establecer un nombre de archivo fijo para el log
    filename = 'logs/sistema.log'

    # Asegurarse de que el directorio 'logs' existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    format = '%(asctime)s - %(levelname)s - %(module)s: %(message)s'
    maxBytes = 10485760  # 10MB
    backupCount = 5

    formatter = logging.Formatter(format)

    # Cambiar a un RotatingFileHandler con un nombre de archivo fijo
    file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)  # Nivel más bajo para capturar todos los logs
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Escribir un delimitador de sesión al inicio de cada ejecución
    logger.info("\n\n--------------- Nueva Sesión - {} ---------------\n\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    return logger
