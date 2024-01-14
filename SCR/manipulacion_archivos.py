#manipulacion_archivos.py
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def filtrar_archivos_por_extension(archivos, extensiones):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones dadas.

    Args:
        archivos (list of str): Lista de nombres de archivos a filtrar.
        extensiones (list of str): Extensiones para usar en el filtrado.

    Returns:
        list of str: Lista de archivos filtrados que coinciden con las extensiones.
    """
    return [archivo for archivo in archivos if any(archivo.endswith(ext) for ext in extensiones)]

def listar_archivos(ruta, extensiones=None):
    """
    Lista los archivos en una ruta dada, opcionalmente filtrando por extensiones.

    Args:
        ruta (str): Ruta del directorio a explorar.
        extensiones (list of str, optional): Extensiones para filtrar archivos. Si es None, lista todos los archivos.

    Returns:
        list of str: Lista de archivos encontrados.
        list of str: Estructura de directorio y archivos.
    """
    archivos_encontrados = []
    estructura = []

    logger.debug(f"Iniciando listado de archivos en la ruta: {ruta}")

    for raiz, _, archivos in os.walk(ruta):
        if '.git' in raiz:  # Ignorar directorios .git
            continue

        nivel = raiz.replace(ruta, '').count(os.sep)
        indentacion = ' ' * 4 * nivel
        estructura.append(f"{indentacion}{os.path.basename(raiz)}/")
        subindentacion = ' ' * 4 * (nivel + 1)

        archivos_en_raiz = [os.path.join(raiz, archivo) for archivo in archivos]
        archivos_filtrados = archivos_en_raiz if extensiones is None else filtrar_archivos_por_extension(archivos_en_raiz, extensiones)
        estructura.extend(f"{subindentacion}{os.path.basename(archivo)}" for archivo in archivos_filtrados)
        archivos_encontrados.extend(archivos_filtrados)

    logger.debug(f"Listado de archivos completo. Total de archivos encontrados: {len(archivos_encontrados)}")

    return archivos_encontrados, estructura
