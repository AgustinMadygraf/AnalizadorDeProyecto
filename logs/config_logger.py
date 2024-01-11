import logging
from logging.handlers import RotatingFileHandler
import datetime

def configurar_logging():
    logger = logging.getLogger()
    if logger.hasHandlers():  # Verificar si ya existen manejadores
        return logger

    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'logs/{fecha_hora_actual}.log'

    format = '%(asctime)s - %(levelname)s - %(module)s: %(message)s'
    maxBytes = 10485760  # 10MB
    backupCount = 5

    formatter = logging.Formatter(format)

    file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)  # Nivel más bajo para capturar todos los logs
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
