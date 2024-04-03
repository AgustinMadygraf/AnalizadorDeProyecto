#src/file_operations.py
import os
from logs.config_logger import configurar_logging

logger = configurar_logging()

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

    extensiones_set = set(extensiones)  # Uso de un conjunto para búsqueda eficiente.
    archivos_especiales = {'Pipfile', 'Pipfile.lock'}
    
    # Filtra archivos por extensión o si están en la lista de archivos especiales.
    return [archivo for archivo in archivos 
            if os.path.splitext(archivo)[1] in extensiones_set or os.path.basename(archivo) in archivos_especiales]

def listar_archivos(ruta, extensiones=None):
    """
    Recorre de manera recursiva la ruta proporcionada, listando todos los archivos y,
    opcionalmente, filtrando por extensiones de archivo.
    
    Args:
        ruta (str): Ruta de la carpeta a escanear.
        extensiones (list, optional): Lista de extensiones de archivo para filtrar. 
                                       Por defecto es None, lo que incluye todos los archivos.
    
    Returns:
        tuple: 
        - (list): Lista de archivos filtrados encontrados.
        - (list): Lista de cadenas representando la estructura de directorios y archivos encontrados.
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

        archivos_temp = [os.path.join(raiz, archivo) for archivo in archivos]
        archivos_filtrados = filtrar_archivos_por_extension(archivos_temp, extensiones)
        estructura.extend(f"{subindentacion}{os.path.basename(archivo)}" for archivo in archivos_filtrados)
        archivos_encontrados.extend(archivos_filtrados)

    return archivos_encontrados, estructura
