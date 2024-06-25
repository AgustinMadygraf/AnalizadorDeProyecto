#AnalizadorDeProyectos/src/file_operations.py
import os
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def contar_lineas_codigo(file_path, extensiones_codigo):
    """
    Cuenta las líneas de código en un archivo, excluyendo líneas en blanco y comentarios.

    Args:
        file_path (str): Ruta del archivo.
        extensiones_codigo (set): Conjunto de extensiones de archivo que representan código fuente.

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
    except Exception as e:
        logger.error(f"Error leyendo el archivo {file_path}: {e}")
        return None

    # Asegurarse de que el número de líneas sea de 3 dígitos
    if lineas_codigo == 0:
        return None
    elif lineas_codigo > 999:
        return 999
    else:
        return lineas_codigo

def listar_archivos(ruta, extensiones_permitidas):
    """
    Recorre de manera recursiva la ruta proporcionada, listando todos los archivos y,
    opcionalmente, filtrando por extensiones de archivo. Además, incluye el peso de cada
    archivo en kilobytes y el número de líneas de código.

    Args:
        ruta (str): Ruta de la carpeta a escanear.
        extensiones (list, optional): Lista de extensiones de archivo para filtrar. 
                                       Por defecto es None, lo que incluye todos los archivos.

    Returns:
        tuple: 
        - (list): Lista de archivos filtrados encontrados.
        - (list): Lista de cadenas representando la estructura de directorios y archivos encontrados, incluyendo el peso de cada archivo en kB y el número de líneas de código.
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
            if not extensiones_permitidas or os.path.splitext(archivo)[1] in extensiones_permitidas or archivo in {'Pipfile', 'Pipfile.lock'}:
                archivos_encontrados.append(archivo_completo)
                # Obtiene el tamaño del archivo en kilobytes
                tamano_kb = os.path.getsize(archivo_completo) / 1024
                espacio_vacio = ' ' * (50 - len(archivo) - len(subindentacion))
                lineas_codigo = contar_lineas_codigo(archivo_completo, {'.py', '.ino', '.h'})
                if lineas_codigo is None:
                    estructura.append(f"{subindentacion}{os.path.basename(archivo)}{espacio_vacio}{tamano_kb:.2f}kB - N/A")
                else:
                    estructura.append(f"{subindentacion}{os.path.basename(archivo)}{espacio_vacio}{tamano_kb:.2f}kB - {lineas_codigo:03d} líneas de código")
    return archivos_encontrados, estructura
