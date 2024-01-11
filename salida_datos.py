import os
import datetime
from gestion_archivos import leer_archivo, copiar_contenido_al_portapapeles
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def generar_nombre_archivo_salida(ruta, nombre_base='listado'):
    """
    Genera el nombre del archivo de salida basado en la ruta y un nombre base.

    Args:
        ruta (str): Ruta del directorio para el archivo de salida.
        nombre_base (str): Nombre base para el archivo de salida.

    Returns:
        str: Ruta completa del archivo de salida.
    """
    # Formatear la ruta para el nombre del archivo
    ruta_formateada = ruta.replace("\\", "%").replace(":", "_")
    print("\n\n ruta_formateada: ",ruta_formateada,"\n\n")
    nombre_archivo_salida = f"[LIST]-{ruta_formateada}.txt"
    print("\n\n nombre_archivo_salida: ",nombre_archivo_salida,"\n\n")

    return os.path.join(ruta, nombre_archivo_salida)


def escribir_archivo_salida(nombre_archivo, contenido):
    """
    Escribe el contenido dado en el archivo de salida especificado.

    Args:
        nombre_archivo (str): Ruta del archivo donde se escribirá el contenido.
        contenido (str): Contenido a escribir en el archivo.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        logger.info(f"Archivo de salida generado: {nombre_archivo}")
    except Exception as e:
        logger.error(f"Error al escribir en el archivo de salida {nombre_archivo}: {e}")

def preparar_contenido_salida(estructura, modo_prompt):
    """
    Prepara el contenido del archivo de salida.

    Args:
        estructura (list): Estructura de directorios y archivos a incluir.
        modo_prompt (str): Modo seleccionado para la salida.

    Returns:
        str: Contenido formateado para el archivo de salida.
    """
    contenido_prompt = leer_archivo(modo_prompt) if modo_prompt else ''
    fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contenido = f"Fecha y hora de generación: {fecha_hora_actual}\n\n"
    contenido += contenido_prompt + "\n\n" if contenido_prompt else ''
    contenido += "\n\nEstructura de Carpetas y Archivos:\n"
    contenido += '\n'.join(estructura) + "\n\n"
    return contenido

def generar_archivo_salida(ruta, archivos, estructura, modo_prompt):
    """
    Genera el archivo de salida con la estructura dada.

    Args:
        ruta (str): Ruta del directorio donde se generará el archivo de salida.
        estructura (list): Estructura de directorios y archivos a incluir en el archivo de salida.
        modo_prompt (str): Modo seleccionado para la salida.
    """
    nombre_archivo_salida = generar_nombre_archivo_salida(ruta)
    print("\n\n\n nombre_archivo_salida: ",nombre_archivo_salida)
    contenido = preparar_contenido_salida(estructura, modo_prompt)
    escribir_archivo_salida(nombre_archivo_salida, contenido)
    copiar_contenido_al_portapapeles(nombre_archivo_salida)

    return(nombre_archivo_salida)

# Ejemplo de uso
# ruta = 'ruta/a/tu/directorio'
# estructura = ['Directorio1/', '   archivo1.txt', 'Directorio2/', '   archivo2.txt']
# modo_prompt = 'ruta/a/tu/modo_prompt.txt'
# generar_archivo_salida(ruta, estructura, modo_prompt)
