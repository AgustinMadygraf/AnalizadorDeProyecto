import pyperclip
import logging
import os

logging.basicConfig(filename='logs/gestion_archivos.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def leer_archivo(nombre_archivo):
    """
    Lee el contenido de un archivo y lo devuelve.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.

    Returns:
        str: Contenido del archivo.
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            logging.debug(f"Archivo '{nombre_archivo}' leído exitosamente.")
            return contenido
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {nombre_archivo}")
        return None
    except IOError as e:
        logging.error(f"Error de E/S al leer el archivo {nombre_archivo}: {e}")
        return None
    except UnicodeDecodeError as e:
        logging.error(f"Error de decodificación al leer el archivo {nombre_archivo}: {e}")
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
            logging.info(f"El contenido del archivo '{nombre_archivo_salida}' ha sido copiado al portapapeles.")
        except pyperclip.PyperclipException as e:
            logging.error(f"No se pudo copiar al portapapeles: {e}")

def verificar_existencia_archivo(nombre_archivo):
    """
    Verifica si un archivo existe.

    Args:
        nombre_archivo (str): Ruta del archivo a verificar.

    Returns:
        bool: True si el archivo existe, False en caso contrario.
    """
    return os.path.exists(nombre_archivo)
