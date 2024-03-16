#SCR/UtilSist.py
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
