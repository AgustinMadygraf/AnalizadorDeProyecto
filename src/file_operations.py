#src/data_output.py
import os
from logs.config_logger import configurar_logging

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
                espacio_vacio = ' ' * (50 - len(archivo) - len(subindentacion))
                lineas_codigo = contar_lineas_codigo(archivo_completo, {'.py', '.ipynb'})
                estructura.append(f"{subindentacion}{os.path.basename(archivo)}{espacio_vacio}{tamano_kb:.2f}kB - {lineas_codigo}")
    return archivos_encontrados, estructura

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

def contar_lineas_codigo(file_path, extensiones_codigo):
    """
    Cuenta las líneas de código en un archivo, excluyendo líneas en blanco y comentarios.

    Args:
        file_path (str): Ruta del archivo.
        extensiones_codigo (set): Conjunto de extensiones de archivo que representan código fuente.

    Returns:
        int: Número de líneas de código.
    """
    _, extension = os.path.splitext(file_path)
    if extension not in extensiones_codigo:
        return 0

    lineas_codigo = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea and not linea.startswith("#"):
                    lineas_codigo += 1
    except Exception as e:
        logger.error(f"Error leyendo el archivo {file_path}: {e}")
    return lineas_codigo