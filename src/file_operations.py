import os
from logs.config_logger import configurar_logging

logger = configurar_logging()

def filtrar_archivos_por_extension(archivos, extensiones):
    if not extensiones:  # Si no se proporcionan extensiones, devolver todos los archivos
        return archivos
    extensiones_set = set(extensiones)  # Convertir lista a conjunto para búsqueda eficiente
    archivos_especiales = {'Pipfile', 'Pipfile.lock'}
    return [archivo for archivo in archivos if os.path.splitext(archivo)[1] in extensiones_set or os.path.basename(archivo) in archivos_especiales]


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
