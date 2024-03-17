#src/utilities.py
import sys
from importlib import metadata
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def obtener_version_python():
    return sys.version

def limpieza_pantalla(habilitar=True):
    """
    Limpia la pantalla de la consola, si está habilitado.

    Args:
        habilitar (bool): Indica si la función de limpieza está habilitada.
    """
    if not habilitar:
        logger.debug("Limpieza de pantalla deshabilitada.")
        return

    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        logger.debug("Pantalla limpiada.")
    except Exception as e:
        logger.error(f"No se pudo limpiar la pantalla: {e}")

def leer_contenido_archivo(ruta_archivo):
    """
    Lee el contenido de un archivo dado por su ruta.
    
    Args:
        ruta_archivo (str): La ruta completa al archivo.
    
    Returns:
        str: El contenido del archivo.
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        # Considerar manejo específico de excepciones o registro
        print(f"Error al leer el archivo: {e}")
        return None
