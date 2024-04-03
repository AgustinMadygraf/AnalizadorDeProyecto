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