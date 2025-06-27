# Este archivo contiene la implementación adaptada de operaciones de archivos
# Originalmente en src/file_operations.py, ahora movido a infraestructura

# Eliminar imports no utilizados
import os

def listar_archivos(ruta, extensiones_permitidas):
    """
    Implementación movida desde src/file_operations.py
    """
    archivos_encontrados = []
    estructura = []

    for raiz, _, archivos in os.walk(ruta):
        if '.git' in raiz:
            continue

        nivel = raiz.replace(ruta, '').count(os.sep)
        estructura.append(f"{' ' * 4 * nivel}{os.path.basename(raiz)}/")

        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            if not extensiones_permitidas or os.path.splitext(archivo_completo)[1] in extensiones_permitidas:
                archivos_encontrados.append(archivo_completo)
                estructura.append(f"{' ' * 4 * (nivel + 1)}{os.path.basename(archivo_completo)}")

    return archivos_encontrados, estructura

def contar_lineas_codigo(file_path, extensiones_codigo, logger):
    """
    Cuenta las líneas de código en un archivo, excluyendo líneas en blanco y comentarios.
    Args:
        file_path (str): Ruta del archivo.
        extensiones_codigo (set): Conjunto de extensiones de archivo que representan código fuente.
        logger: Interfaz para logging.
    Returns:
        int or None: Número de líneas de código (entero de 3 dígitos), o None si el conteo es 0.
    """
    _, extension = os.path.splitext(file_path)
    if extension not in extensiones_codigo:
        return None
    lineas_codigo = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea and not linea.startswith("#"):
                    lineas_codigo += 1
    except (IOError, OSError) as e:
        logger.error(f"Error leyendo el archivo {file_path}: {e}")
        return None
    if lineas_codigo == 0:
        return None
    elif lineas_codigo > 999:
        return 999
    else:
        return lineas_codigo

__all__ = ['listar_archivos', 'contar_lineas_codigo']
