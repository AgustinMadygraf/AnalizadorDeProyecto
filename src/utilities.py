#src/utilities.py
import sys
import os
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().get_logger()

def obtener_version_python():
    return sys.version

def limpieza_pantalla():
    print("\033[H\033[J", end="")
    logger.debug("Pantalla limpiada.")

