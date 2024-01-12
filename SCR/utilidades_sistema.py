# utilidades_sistema.py
import subprocess
import sys
from importlib import metadata
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def obtener_version_python():
    return sys.version

def obtener_librerias_pip():
    logger.info("Obteniendo listado de librerías de pip.")
    resultado = subprocess.run(["pip", "list"], capture_output=True, text=True)
    return resultado.stdout

def limpieza_pantalla():
    logger.info("Limpiando pantalla.")
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
