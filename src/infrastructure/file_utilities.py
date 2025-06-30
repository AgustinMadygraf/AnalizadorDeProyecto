# Migrated from src/file_utilities.py
# ...existing code from file_utilities.py will be placed here...
import os
import logging

logger = logging.getLogger(__name__)

def copiar_contenido_al_portapapeles(file_path_salida, extensiones_permitidas=None):
    """Copia el contenido de un archivo al portapapeles si existe y no está vacío."""
    if not os.path.exists(file_path_salida):
        logger.warning("El archivo '%s' no existe.", file_path_salida)
        return
    with open(file_path_salida, 'r', encoding='utf-8') as f:
        contenido = f.read()
    if contenido:
        try:
            import pyperclip
            pyperclip.copy(contenido)
            logger.info("El contenido del archivo ha sido copiado al portapapeles.")
        except Exception as e:
            logger.error("No se pudo copiar al portapapeles: %s", e)
    else:
        logger.warning("El archivo '%s' está vacío o no se pudo leer.", file_path_salida)
