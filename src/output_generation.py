import os
import datetime
from src.file_manager import leer_archivo, copiar_contenido_al_portapapeles
from src.logs.config_logger import configurar_logging
from src.file_operations_extended import listar_archivos, asegurar_directorio_DOCS

logger = configurar_logging()

def generar_archivo_salida(ruta, modo_prompt, extensiones, ruta_archivos):
    """
    Genera el archivo de salida con la estructura dada.

    Args:
        ruta (str): Ruta del directorio donde se generará el archivo de salida.
        estructura (list): Estructura de directorios y archivos a incluir en el archivo de salida.
        modo_prompt (str): Modo seleccionado para la salida.
        extensiones (list of str): Extensiones para filtrar archivos.
        ruta_proyecto (str): Ruta base del proyecto.
    """
    asegurar_directorio_DOCS(ruta)
    archivos_encontrados, estructura_actualizada = listar_archivos(ruta, extensiones)
    nombre_archivo_salida = generar_nombre_archivo_salida(ruta)
    formatear_archivo_salida(nombre_archivo_salida)
    contenido = preparar_contenido_salida(estructura_actualizada, modo_prompt, archivos_encontrados, ruta, ruta_archivos)
    escribir_archivo_salida(nombre_archivo_salida, contenido)
    copiar_contenido_al_portapapeles(nombre_archivo_salida)
    return nombre_archivo_salida

def formatear_archivo_salida(nombre_archivo_salida):
    """
    Elimina el contenido del archivo de salida.

    Args:
        nombre_archivo_salida (str): Ruta del archivo cuyo contenido se eliminará.
    """
    try:
        # Abrir el archivo en modo de escritura, lo que borrará su contenido
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write('')  # Escribir un contenido vacío
        logger.debug(f"El contenido de {nombre_archivo_salida} ha sido eliminado.")
    except Exception as e:
        logger.warning(f"Error al intentar formatear el archivo {nombre_archivo_salida}: {e}")

def preparar_contenido_salida(estructura, modo_prompt, archivos_seleccionados, ruta, ruta_archivo):
    logger.debug("Preparando contenido de salida")
    
    # Construir el contenido inicial basado en el prompt o proveer un mensaje de error predeterminado
    contenido_prompt = leer_archivo(os.path.join(ruta_archivo, modo_prompt), permiso=True) or "\n\nprompt:\nNo hay prompt. falla.\n\n"
    contenido =  contenido_prompt

    # Añadiendo la estructura de directorios y archivos en formato Markdown.
    contenido += "\n\n## Estructura de Carpetas y Archivos\n```bash\n" + '\n'.join(estructura) + "\n```\n"

    # Procesamiento y adición de contenido de archivos seleccionados.
    if archivos_seleccionados:
        contenido += construir_contenido_archivos_seleccionados(archivos_seleccionados)
    else:
        logger.warning("No se han proporcionado archivos seleccionados para incluir en el contenido")

    contenido += "\nFecha y hora:\n" 
    contenido += datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "\n\n"
    

    return contenido

def construir_contenido_archivos_seleccionados(archivos_seleccionados):
    """Genera la sección de contenido para archivos seleccionados en Markdown."""
    contenido_archivos = "\n\n## Contenido de Archivos Seleccionados\n"
    for archivo in archivos_seleccionados:
        contenido_archivo = leer_archivo(archivo, permiso=True)
        if contenido_archivo:
            # Agregar el contenido del archivo al bloque de Markdown
            contenido_archivos += f"\n### {archivo}\n```plaintext\n{contenido_archivo}\n```\n"
        else:
            logger.warning(f"No se pudo obtener el contenido del archivo: {archivo}")
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

def generar_nombre_archivo_salida(ruta):
    """
    Genera el nombre del archivo de salida basado en la ruta y un nombre base.

    Args:
        ruta (str): Ruta del directorio para el archivo de salida.
        nombre_base (str): Nombre base para el archivo de salida.

    Returns:
        str: Ruta completa del archivo de salida.
    """
    # Formatear la ruta para el nombre del archivo
    nombre_archivo_salida = f"DOCS\\00-Prompt-for-ProjectAnalysis.md" #DOCS = Analysis and Modification Improvement System
    return os.path.join(ruta, nombre_archivo_salida)

def escribir_archivo_salida(nombre_archivo, contenido):
    """
    Escribe el contenido dado en el archivo de salida especificado y maneja los errores de manera más detallada.

    Args:
        nombre_archivo (str): Ruta del archivo donde se escribirá el contenido.
        contenido (str): Contenido a escribir en el archivo.
    """
    print("")
    if contenido is None:
        logger.error(f"Se intentó escribir contenido 'None' en el archivo {nombre_archivo}.")
        return False
    logger.debug(f"Intentando escribir en el archivo: {nombre_archivo}")
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        logger.info(f"Archivo de salida generado exitosamente: {nombre_archivo}")
        return True
    except IOError as e:
        logger.error(f"Error de E/S al escribir en el archivo {nombre_archivo}: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al escribir en el archivo {nombre_archivo}: {e}")
    return False
