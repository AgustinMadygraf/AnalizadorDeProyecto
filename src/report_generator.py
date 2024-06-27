# src/report_generator.py
import os
import datetime
from src.file_utilities import copiar_contenido_al_portapapeles
from src.logs.config_logger import LoggerConfigurator
from src.file_operations import listar_archivos
from src.content_manager import asegurar_directorio_docs
from src.models.file_manager import FileManager

logger = LoggerConfigurator().get_logger()

# Crear una instancia de FileManager
project_path = "C:\\AppServ\\www\\AnalizadorDeProyecto"
file_manager = FileManager(project_path)

def generar_archivo_salida(path, modo_prompt, extensiones_permitidas, ruta_archivos):
    """
    Genera el archivo de salida con la estructura dada.

    Args:
        path(str): Ruta del directorio donde se generará el archivo de salida.
        estructura (list): Estructura de directorios y archivos a incluir en el archivo de salida.
        modo_prompt (str): Modo seleccionado para la salida.
        extensiones (list of str): Extensiones para filtrar archivos.
        project_path (str): Ruta base del proyecto.
    """
    asegurar_directorio_docs(path)
    archivos_encontrados, estructura_actualizada = listar_archivos(path, extensiones_permitidas)
    nombre_archivo_salida = generar_nombre_archivo_salida(path)
    formatear_archivo_salida(nombre_archivo_salida)
    contenido = preparar_contenido_salida(estructura_actualizada, modo_prompt, archivos_encontrados, path, ruta_archivos, extensiones_permitidas)
    escribir_archivo_salida(nombre_archivo_salida, contenido)
    copiar_contenido_al_portapapeles(nombre_archivo_salida, extensiones_permitidas)
    print("")
    return nombre_archivo_salida

def formatear_archivo_salida(nombre_archivo_salida):
    """
    Elimina el contenido del archivo de salida.

    Args:
        nombre_archivo_salida (str): Ruta del archivo cuyo contenido se eliminará.
    """
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write('')  # Escribir un contenido vacío
        logger.debug(f"El contenido de {nombre_archivo_salida} ha sido eliminado.")
    except Exception as e:
        logger.warning(f"Error al intentar formatear el archivo {nombre_archivo_salida}: {e}")

def preparar_contenido_salida(estructura, modo_prompt, archivos_seleccionados, path, ruta_archivo, extensiones_permitidas):
    """
    Prepara el contenido de salida agregando la estructura de directorios y archivos con sus tamaños,
    el contenido de archivos seleccionados, y la fecha y hora actual.

    Args:
        estructura (list): Lista de directorios y archivos con sus tamaños en kB.
        modo_prompt (str): Ruta al archivo de configuración de prompt seleccionado.
        archivos_seleccionados (list): Lista de rutas de archivos seleccionados para mostrar su contenido.
        path(str): Ruta base donde se encuentra el proyecto.
        ruta_archivo (str): Ruta donde se encuentran los archivos de configuración.

    Returns:
        str: El contenido completo a ser presentado o guardado.
    """
    logger.debug("Preparando contenido de salida")

    # Intentar leer el contenido del archivo de prompt, si no es posible, usar un mensaje de error predeterminado.
    contenido_prompt = file_manager.read_and_validate_file(os.path.join(ruta_archivo, modo_prompt), permitir_lectura=True, extensiones_permitidas=extensiones_permitidas) or "\n\nPrompt:\nNo hay prompt. Falla.\n\n"    
    contenido = contenido_prompt
    # Verificar si existe todo.txt y añadir su contenido
    ruta_todo_txt = os.path.join(path, 'todo.txt')
    if os.path.exists(ruta_todo_txt):
        with open(ruta_todo_txt, 'r', encoding='utf-8') as todo_file:
            contenido_todo_txt = todo_file.read()
            contenido += "\n## TODO List from todo.txt\n" + contenido_todo_txt + "\n"

    # Añadiendo directamente la estructura de carpetas y archivos, incluyendo el tamaño de cada archivo.
    contenido += "\n\n## Estructura de Carpetas y Archivos\n```bash\n" + '\n'.join(estructura) + "\n```\n"

    # Procesar y añadir el contenido de archivos seleccionados, si los hay.
    if archivos_seleccionados:
        contenido += construir_contenido_archivos_seleccionados(archivos_seleccionados, extensiones_permitidas)
    else:
        logger.warning("No se han proporcionado archivos seleccionados para incluir en el contenido")

    # Añadir la fecha y hora actuales al contenido.
    contenido += "Fecha y hora:\n"
    contenido += datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n\n"
    
    return contenido

def construir_contenido_archivos_seleccionados(archivos_seleccionados, extensiones_permitidas):
    """Genera la sección de contenido para archivos seleccionados en Markdown."""
    contenido_archivos = "\n\n## Contenido de Archivos Seleccionados\n"
    for archivo in archivos_seleccionados:
        contenido_archivo = file_manager.read_and_validate_file(archivo, True, extensiones_permitidas)
        if contenido_archivo:
            # Agregar el contenido del archivo al bloque de Markdown
            contenido_archivos += f"\n### {archivo}\n```plaintext\n{contenido_archivo}\n```\n"
        else:
            logger.debug(f"No se pudo obtener el contenido del archivo: {archivo}")
    return contenido_archivos

def escapar_caracteres_md(texto):
    """
    Escapa caracteres especiales de Markdown en un texto.

    Args:
        texto (str): Texto a escapar.

    Returns:
        str: Texto con caracteres de Markdown escapados.
    """
    # Lista de caracteres que pueden interferir con el formato Markdown.
    caracteres_a_escapar = ['*', '_', '`', '!', '[', ']', '(', ')']
    for char in caracteres_a_escapar:
        texto = texto.replace(char, f'\\{char}')
    return texto

def generar_nombre_archivo_salida(path):
    """
    Genera el nombre del archivo de salida basado en la ruta y un nombre base.

    Args:
        path(str): Ruta del directorio para el archivo de salida.
        nombre_base (str): Nombre base para el archivo de salida.

    Returns:
        str: Ruta completa del archivo de salida.
    """
    nombre_archivo_salida = f"docs\\00-Prompt-for-ProjectAnalysis.md"
    return os.path.join(path, nombre_archivo_salida)

def escribir_archivo_salida(nombre_archivo, contenido):
    """
    Escribe el contenido dado en el archivo de salida especificado y maneja los errores de manera más detallada.

    Args:
        nombre_archivo (str): Ruta del archivo donde se escribirá el contenido.
        contenido (str): Contenido a escribir en el archivo.
    """
    if contenido is None:
        logger.error(f"Se intentó escribir contenido 'None' en el archivo {nombre_archivo}.")
        return False
    logger.debug(f"Intentando escribir en el archivo: {nombre_archivo}")
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        logger.info("Archivo de salida generado exitosamente:")
        logger.info(nombre_archivo)
        return True
    except IOError as e:
        logger.error(f"Error de E/S al escribir en el archivo {nombre_archivo}: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al escribir en el archivo {nombre_archivo}: {e}")
    return False
