#src/data_output.py
import os
import time
from file_manager import leer_archivo, copiar_contenido_al_portapapeles
from logs.config_logger import configurar_logging
import logging

# Configuración del logger
logger = configurar_logging()

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
    
def listar_archivos(ruta, extensiones):
    """
    Recorre de manera recursiva la ruta proporcionada, listando todos los archivos y,
    opcionalmente, filtrando por extensiones de archivo. Además, incluye el peso de cada
    archivo en kilobytes.
    
    Args:
        ruta (str): Ruta de la carpeta a escanear.
        extensiones (list, optional): Lista de extensiones de archivo para filtrar. 
                                       Por defecto es None, lo que incluye todos los archivos.
    
    Returns:
        tuple: 
        - (list): Lista de archivos filtrados encontrados.
        - (list): Lista de cadenas representando la estructura de directorios y archivos encontrados, incluyendo el peso de cada archivo en kB.
    """
    archivos_encontrados = []
    estructura = []

    for raiz, _, archivos in os.walk(ruta):
        if '.git' in raiz:  # Ignora directorios .git
            continue

        nivel = raiz.replace(ruta, '').count(os.sep)
        indentacion = ' ' * 4 * nivel
        estructura.append(f"{indentacion}{os.path.basename(raiz)}/")
        subindentacion = ' ' * 4 * (nivel + 1)

        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            if not extensiones or os.path.splitext(archivo)[1] in extensiones or archivo in {'Pipfile', 'Pipfile.lock'}:
                archivos_encontrados.append(archivo_completo)
                # Obtiene el tamaño del archivo en kilobytes
                tamano_kb = os.path.getsize(archivo_completo) / 1024
                estructura.append(f"{subindentacion}{os.path.basename(archivo)} - {tamano_kb:.2f}kB")

    return archivos_encontrados, estructura

def filtrar_archivos_por_extension(archivos, extensiones):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones dadas.

    Parámetros:
    archivos (list of str): Lista de nombres de archivos a filtrar.
    extensiones (list of str): Extensiones para usar en el filtrado.

    Retorna:
    list of str: Lista de archivos filtrados que coinciden con las extensiones.
    """
    extensiones_set = set(ext.lower() for ext in extensiones)
    archivos_filtrados = [archivo for archivo in archivos if any(archivo.lower().endswith(ext) for ext in extensiones_set)]
    return archivos_filtrados

def asegurar_directorio_DOCS(ruta):
    """
    Asegura que exista el directorio DOCS en la ruta dada.
    Si el directorio no existe, lo crea.

    Args:
        ruta (str): Ruta base donde se debe encontrar o crear el directorio DOCS.
    """
    directorio_DOCS = os.path.join(ruta, 'DOCS')
    if not os.path.exists(directorio_DOCS):
        os.makedirs(directorio_DOCS)
        logger.info(f"Directorio DOCS creado en {directorio_DOCS}")
    else:
        logger.debug(f"Directorio DOCS ya existe en {directorio_DOCS}")
