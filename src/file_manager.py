#src/file_manager.py
import pyperclip
import os
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

def validar_file_name(file_name):
    """Valida el tipo de dato del nombre del archivo."""
    if not isinstance(file_name, str):
        logger.warning(f"Tipo de dato incorrecto para file_name: {type(file_name)}. Se esperaba una cadena (str).")
        return False
    return True

def archivo_permitido(file_name, extensiones_permitidas):
    file_name_puro = os.path.basename(file_name)
    archivos_especificamente_permitidos = {'Pipfile', 'Pipfile.lock'}
    # Verifica si el archivo es específicamente permitido o si su extensión está en la lista de permitidas
    return file_name_puro in archivos_especificamente_permitidos or \
           any(file_name_puro.endswith(ext) for ext in extensiones_permitidas)



def leer_contenido_archivo(file_name):
    """Lee el contenido de un archivo de texto.

    Args:
        file_name (str): Ruta completa al archivo que se va a leer.

    Returns:
        str: Contenido del archivo, o None si ocurre un error o si el archivo no cumple con los requisitos de seguridad.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        logger.error(f"No se pudo leer el archivo {file_name}: {e}")
        return None

def read_file(file_name,permiso, extensiones_permitidas=['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt', '.ino']):
    """Orquesta la validación del nombre de archivo y su lectura si es permitido."""
    if not validar_file_name(file_name) or not os.path.isfile(file_name):
        return None

    if not archivo_permitido(file_name, extensiones_permitidas):
        logger.debug(f"Extensión de archivo no permitida para lectura: {file_name}")
        return None

    if permiso:
        if '..' in os.path.abspath(file_name) or "docs" in file_name:
            logger.debug("Acceso a archivo fuera del directorio permitido o intento de leer archivo en directorio 'docs'.")
            return None
        
        if os.path.getsize(file_name) > 10240:
            logger.warning(f"El archivo '{file_name}' excede el tamaño máximo permitido de 10KB.")
            return None

    if esta_en_gitignore(file_name, ruta_proyecto):
        logger.warning(f"El archivo '{file_name}' está listado en .gitignore y no será leído.")
        return None

    return leer_contenido_archivo(file_name)


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

def copiar_contenido_al_portapapeles(file_name_salida):
    """
    Copia el contenido de un archivo al portapapeles.

    Args:
        file_name_salida (str): Ruta del archivo cuyo contenido se copiará.
    """
    # Verificar si el archivo existe
    if not os.path.exists(file_name_salida):
        logger.error(f"El archivo '{file_name_salida}' no existe.")
        return
    permiso = False
    contenido = read_file(file_name_salida,permiso)
    if contenido:
        try:
            pyperclip.copy(contenido)
            logger.info(f"El contenido del archivo ha sido copiado al portapapeles.")
        except pyperclip.PyperclipException as e:
            logger.error(f"No se pudo copiar al portapapeles: {e}")
    else:
        logger.warning(f"El archivo '{file_name_salida}' está vacío o no se pudo leer.")

def verificar_existencia_archivo(file_name):
    """
    Verifica si un archivo existe.

    Args:
        file_name (str): Ruta del archivo a verificar.

    Returns:
        bool: True si el archivo existe, False en caso contrario.
    """
    return os.path.exists(file_name)
