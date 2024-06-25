#src/utilities.py
import sys
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def obtener_version_python():
    return sys.version

def limpieza_pantalla():
    print("\033[H\033[J", end="")
    logger.debug("Pantalla limpiada.")

