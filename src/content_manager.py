# src/content_manager.py
import os
from src.logs.config_logger import LoggerConfigurator

# Configuración del logger
logger = LoggerConfigurator().get_logger()

def contenido_archivo(archivos_seleccionados):
    """
    Concatena el contenido de una lista de archivos seleccionados en un solo string.

    Esta función itera sobre una lista de rutas de archivos, leyendo y agregando el contenido de cada uno a una cadena.
    En caso de un error durante la lectura de un archivo (por ejemplo, si el archivo no existe o no es accesible),
    se agrega un mensaje de error específico a la cadena resultante.

    Args:
        archivos_seleccionados (list of str): Una lista de rutas de archivos cuyos contenidos se desean concatenar.

    Returns:
        str: Una cadena que contiene el contenido concatenado de todos los archivos seleccionados, 
             con cada contenido de archivo precedido por un encabezado que indica el nombre del archivo,
             y seguido de cualquier mensaje de error que ocurra durante la lectura de los archivos.

    Nota:
        Esta función está diseñada para manejar texto. No es adecuada para archivos binarios.
    """
    contenido_total = ""

    # Itera a través de cada archivo en la lista de archivos seleccionados
    for archivo in archivos_seleccionados:
        try:
            # Intenta leer el contenido del archivo
            with open(archivo, 'r', encoding='utf-8') as file:
                contenido = file.read()
                # Añade un encabezado y el contenido del archivo a la cadena total
                contenido_total += f"\n--- Contenido de {archivo} ---\n"
                contenido_total += contenido + "\n"
        except Exception as e:
            # En caso de error, añade un mensaje de error a la cadena total
            contenido_total += f"\nError al leer el archivo {archivo}: {e}\n"

    return contenido_total
    
def filtrar_archivos_por_extension(archivos, extensiones):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones proporcionadas.

    Args:
        archivos (list): Lista de rutas completas a los archivos a filtrar.
        extensiones (list): Lista de extensiones para incluir en el filtrado.

    Returns:
        list: Lista de archivos filtrados que coinciden con las extensiones proporcionadas.
    """
    if not extensiones:  # Devuelve todos los archivos si no se especifican extensiones.
        return archivos

    extensiones_set = set(ext.lower() for ext in extensiones)  # Uso de un conjunto para búsqueda eficiente.
    archivos_especiales = {'pipfile', 'pipfile.lock'}
    
    # Filtra archivos por extensión o si están en la lista de archivos especiales.
    return [archivo for archivo in archivos 
            if os.path.splitext(archivo)[1].lower() in extensiones_set or os.path.basename(archivo).lower() in archivos_especiales]

def asegurar_directorio_docs(ruta):
    """
    Asegura que exista el directorio docs en la ruta dada.
    Si el directorio no existe, lo crea.

    Args:
        ruta (str): Ruta base donde se debe encontrar o crear el directorio docs.
    """
    directorio_docs = os.path.join(ruta, 'docs')
    if not os.path.exists(directorio_docs):
        os.makedirs(directorio_docs)
        logger.debug(f"Directorio docs creado en {directorio_docs}")
    else:
        logger.debug(f"Directorio docs ya existe en {directorio_docs}")
