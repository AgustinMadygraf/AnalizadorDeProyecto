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
    Genera una lista de archivos y su estructura de directorio basada en una ruta y extensiones específicas.

    Esta función recorre recursivamente todos los directorios y subdirectorios a partir de una ruta dada,
    filtrando los archivos según las extensiones proporcionadas. Ignora explícitamente los directorios '.git'.
    Genera dos listas: una con las rutas completas de los archivos filtrados y otra con la estructura
    de directorios y archivos representada en forma de texto para su presentación.

    Args:
        ruta (str): La ruta del directorio raíz desde donde iniciar el escaneo de archivos.
        extensiones (list of str): Una lista de extensiones de archivo para filtrar los archivos.

    Returns:
        tuple: 
            - Una lista de rutas completas de archivos que cumplen con las extensiones dadas.
            - Una lista de cadenas que representa la estructura de directorios y archivos.
            
    Raises:
        Exception: Proporciona información sobre cualquier error que ocurra durante la ejecución de la función.
    """
    try:
        archivos_encontrados = []
        estructura = []

        for raiz, _, archivos in os.walk(ruta):
            # Ignora los directorios .git
            if '.git' in raiz:
                continue

            # Calcula el nivel de indentación basado en la profundidad del directorio.
            nivel = raiz.replace(ruta, '').count(os.sep)
            indentacion = ' ' * 4 * nivel
            estructura.append(f"{indentacion}{os.path.basename(raiz)}/")

            # Aplica una subindentación para los archivos dentro de cada directorio.
            subindentacion = ' ' * 4 * (nivel + 1)

            # Filtra y procesa los archivos en el directorio actual.
            archivos_en_raiz = [os.path.join(raiz, archivo) for archivo in archivos]
            archivos_filtrados = filtrar_archivos_por_extension(archivos_en_raiz, extensiones)
            estructura.extend(f"{subindentacion}{os.path.basename(archivo)}" for archivo in archivos_filtrados)
            archivos_encontrados.extend(archivos_filtrados)

        return archivos_encontrados, estructura
    except Exception as e:
        logger.error(f"Error al listar archivos en {ruta}: {e}")
        return [], []

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
