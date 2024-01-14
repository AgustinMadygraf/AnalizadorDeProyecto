#SCR/GestArch.py
import pyperclip
import os
import time
import fnmatch
import re
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()
ruta_proyecto = "C:\AppServ\www\AnalizadorDeProyecto"

def esta_en_gitignore(ruta_archivo, ruta_proyecto):
    """
    Verifica si un archivo está listado en .gitignore utilizando expresiones regulares para mejorar la eficiencia.

    Args:
        ruta_archivo (str): Ruta del archivo a verificar.
        ruta_proyecto (str): Ruta del directorio del proyecto que contiene .gitignore.

    Returns:
        bool: True si el archivo está en .gitignore, False en caso contrario.
    """
    ruta_gitignore = os.path.join(ruta_proyecto, '.gitignore')
    try:
        with open(ruta_gitignore, 'r', encoding='utf-8') as gitignore:
            gitignore_content = gitignore.read()
            # Crear una expresión regular basada en cada línea del .gitignore
            for pattern in gitignore_content.splitlines():
                regex = fnmatch.translate(pattern.strip())
                if re.match(regex, ruta_archivo):
                    return True
    except FileNotFoundError:
        logger.warning(f"No se encontró el archivo .gitignore en {ruta_proyecto}")
    return False

def leer_archivo(nombre_archivo, extensiones_permitidas=['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt']):
    """
    Lee el contenido de un archivo de texto y lo devuelve.

    Args:
        nombre_archivo (str): Ruta del archivo a leer.
        extensiones_permitidas (list): Lista de extensiones permitidas para leer.

    Returns:
        str: Contenido del archivo.
    """
    # Validación del tipo de 'nombre_archivo'
    if not isinstance(nombre_archivo, str):
        logger.warning(f"Tipo de dato incorrecto para nombre_archivo: {type(nombre_archivo)}. Se esperaba una cadena (str).")
        return None

    # Validación de la extensión del archivo
    if not any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas):
        logger.warning(f"Extensión de archivo no permitida para lectura: {nombre_archivo}")
        return None

    #Validación de la ruta del archivo (debe ser un archivo y no un directorio)
    if not os.path.isfile(nombre_archivo):
        logger.warning(f"El nombre del archivo no corresponde a un archivo: {nombre_archivo}")
        return None

    if esta_en_gitignore(nombre_archivo, ruta_proyecto):
        logger.warning(f"El archivo '{nombre_archivo}' está listado en .gitignore y no será leído.")
        return None
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            logger.debug(f"Archivo '{nombre_archivo}' leído exitosamente.")
            return contenido
    except (FileNotFoundError, OSError, UnicodeDecodeError) as e:
        # Manejo unificado de errores de lectura de archivo y decodificación
        logger.error(f"Error al leer el archivo {nombre_archivo}: {e}")
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
            time.sleep(1)
            print("")
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
