import os
from logs.config_logger import configurar_logging

logger = configurar_logging()

def filtrar_archivos_por_extension(archivos, extensiones):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones dadas,
    utilizando un conjunto para una búsqueda más eficiente.

    Args:
        archivos (list of str): Lista de nombres de archivos a filtrar.
        extensiones (list of str): Extensiones para usar en el filtrado.

    Returns:
        list of str: Lista de archivos filtrados que coinciden con las extensiones.
    """
    if not extensiones:  # Si no se proporcionan extensiones, devolver todos los archivos
        return archivos
    extensiones_set = set(extensiones)  # Convertir lista a conjunto para búsqueda eficiente
    return [archivo for archivo in archivos if os.path.splitext(archivo)[1] in extensiones_set]

def listar_archivos(ruta, extensiones=None):
    """Listar archivos en una ruta dada, opcionalmente filtrados por extensiones."""
    archivos_encontrados = []
    estructura = []

    for raiz, _, archivos in os.walk(ruta):
        if '.git' in raiz:  # Ignorar directorios .git
            continue

        nivel = raiz.replace(ruta, '').count(os.sep)
        indentacion = ' ' * 4 * nivel
        estructura.append(f"{indentacion}{os.path.basename(raiz)}/")
        subindentacion = ' ' * 4 * (nivel + 1)

        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            archivos_encontrados.append(archivo_completo)

    archivos_filtrados = filtrar_archivos_por_extension(archivos_encontrados, extensiones)
    estructura.extend(f"{subindentacion}{os.path.basename(archivo)}" for archivo in archivos_filtrados)

    return archivos_filtrados, estructura
