import pyperclip
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def leer_archivo(nombre_archivo, extensiones_permitidas=['.html', '.css', '.php', '.py', '.json', '.sql', '.me', '.txt']):
    """
    Lee el contenido de un archivo de texto y lo devuelve.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.
        extensiones_permitidas (list): Lista de extensiones permitidas para leer.

    Returns:
        str: Contenido del archivo.
    """
    if not isinstance(nombre_archivo, str):
        logger.error(f"Tipo de dato incorrecto para nombre_archivo: {type(nombre_archivo)}. Se esperaba una cadena (str).")
        return None

    print("\n\nnombre_archivo: ", nombre_archivo, "\n\n")
    
    # Comprobar si la extensión del archivo está en la lista de extensiones permitidas
    if not any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas):
        logger.info(f"Extensión de archivo no permitida para lectura: {nombre_archivo}")
        return None

    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            logger.debug(f"Archivo '{nombre_archivo}' leído exitosamente.")
            return contenido
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {nombre_archivo}")
        return None
    except IOError as e:
        logger.error(f"Error de E/S al leer el archivo {nombre_archivo}: {e}")
        return None
    except UnicodeDecodeError as e:
        logger.error(f"Error de decodificación al leer el archivo {nombre_archivo}: {e}")
        return None


def copiar_contenido_al_portapapeles(nombre_archivo_salida):
    """
    Copia el contenido de un archivo al portapapeles.

    Args:
        nombre_archivo_salida (str): Ruta del archivo cuyo contenido se copiará.
    """
    contenido = leer_archivo(nombre_archivo_salida)
    if contenido is not None:
        try:
            pyperclip.copy(contenido)
            logger.info(f"El contenido del archivo '{nombre_archivo_salida}' ha sido copiado al portapapeles.")
        except pyperclip.PyperclipException as e:
            logger.error(f"No se pudo copiar al portapapeles: {e}")

def verificar_existencia_archivo(nombre_archivo):
    """
    Verifica si un archivo existe.

    Args:
        nombre_archivo (str): Ruta del archivo a verificar.

    Returns:
        bool: True si el archivo existe, False en caso contrario.
    """
    return os.path.exists(nombre_archivo)
