# Este archivo contiene la implementación adaptada de operaciones de archivos
# Originalmente en src/file_operations.py, ahora movido a infraestructura

# Eliminar imports no utilizados
import os

def listar_archivos(ruta, extensiones_permitidas, logger=None):
    """
    Lista archivos y carpetas, agregando para cada archivo .py el número de líneas de código y el tamaño en kB.
    Excluye carpetas __pycache__ y .git. Muestra LOC y kB alineados en columnas.
    """
    archivos_encontrados = []
    estructura = []
    extensiones_codigo = {'.py'}
    ANCHO_NOMBRE = 40
    ANCHO_LOC = 10
    ANCHO_KB = 10

    for raiz, _, archivos in os.walk(ruta):
        # Excluir carpetas .git y __pycache__
        if '.git' in raiz or '__pycache__' in raiz:
            continue

        nivel = raiz.replace(ruta, '').count(os.sep)
        estructura.append(f"{' ' * 4 * nivel}{os.path.basename(raiz)}/")

        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            if not extensiones_permitidas or os.path.splitext(archivo_completo)[1] in extensiones_permitidas:
                archivos_encontrados.append(archivo_completo)
                extension = os.path.splitext(archivo_completo)[1]
                size_kb = os.path.getsize(archivo_completo) / 1024
                size_str = f"{size_kb:6.1f} kB"
                if extension == '.py':
                    loc = contar_lineas_codigo(archivo_completo, extensiones_codigo, logger) if logger else None
                    loc_str = f"{str(loc).rjust(4)} LOC" if loc is not None else "    "
                else:
                    loc_str = " " * ANCHO_LOC
                estructura.append(f"{' ' * 4 * (nivel + 1)}{os.path.basename(archivo_completo):<{ANCHO_NOMBRE}}{loc_str:>{ANCHO_LOC}}{size_str:>{ANCHO_KB}}")

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
