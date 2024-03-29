#src/file_manager.py
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

def validar_nombre_archivo(nombre_archivo):
    """Valida el tipo de dato del nombre del archivo."""
    if not isinstance(nombre_archivo, str):
        logger.warning(f"Tipo de dato incorrecto para nombre_archivo: {type(nombre_archivo)}. Se esperaba una cadena (str).")
        return False
    return True

def archivo_permitido(nombre_archivo, extensiones_permitidas):
    """Verifica si el archivo tiene una extensión permitida."""
    return any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas)

def leer_contenido_archivo(nombre_archivo):
    """Lee y retorna el contenido de un archivo de texto."""
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
        logger.error(f"Error al leer el archivo {nombre_archivo}: {e}")
        return None

def leer_archivo(nombre_archivo, extensiones_permitidas=['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt']):
    """Orquesta la validación del nombre de archivo y su lectura si es permitido."""
    if not validar_nombre_archivo(nombre_archivo) or not os.path.isfile(nombre_archivo):
        return None

    if not archivo_permitido(nombre_archivo, extensiones_permitidas):
        logger.warning(f"Extensión de archivo no permitida para lectura: {nombre_archivo}")
        return None

    if '..' in os.path.abspath(nombre_archivo) or "DOCS" in nombre_archivo:
        logger.error("Acceso a archivo fuera del directorio permitido o intento de leer archivo en directorio 'DOCS'.")
        return None

    if esta_en_gitignore(nombre_archivo, ruta_proyecto):
        logger.warning(f"El archivo '{nombre_archivo}' está listado en .gitignore y no será leído.")
        return None

    if os.path.getsize(nombre_archivo) > 10240:
        logger.warning(f"El archivo '{nombre_archivo}' excede el tamaño máximo permitido de 10KB.")
        return None

    return leer_contenido_archivo(nombre_archivo)


def procesar_sql(contenido_sql):
    lineas = contenido_sql.split('\n')
    lineas_procesadas = []
    dentro_de_insert = False
    for linea in lineas:
        if 'INSERT INTO' in linea:
            dentro_de_insert = True
            lineas_procesadas.append(linea)  # Añadir la primera línea del INSERT
        elif dentro_de_insert and ';' in linea:
            lineas_procesadas.append(linea)  # Añadir la última línea del INSERT
            dentro_de_insert = False
        elif dentro_de_insert:
            # Opcional: Añadir alguna indicación de que se han omitido líneas
            pass
    return '\n'.join(lineas_procesadas)

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
