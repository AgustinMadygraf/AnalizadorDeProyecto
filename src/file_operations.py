# Mover este archivo a src/infrastructure/file_operations_adapter.py
# Actualizar imports en todo el proyecto para reflejar la nueva ubicación

import os
from src.infrastructure.file_operations_adapter import contar_lineas_codigo
from src.infrastructure.logger_adapter import LoggerAdapter
from src.interfaces.logger_port import LoggerPort

# Initialize a logger instance
logger: LoggerPort = LoggerAdapter()

def listar_archivos(ruta, extensiones_permitidas):
    """
    Recorre de manera recursiva la ruta proporcionada, listando todos los archivos y,
    opcionalmente, filtrando por extensiones de archivo. Además, incluye el peso de cada
    archivo en kilobytes y el número de líneas de código.

    Args:
        ruta (str): Ruta de la carpeta a escanear.
        extensiones_permitidas (list, optional): Lista de extensiones de archivo para filtrar. 
                                       Por defecto es None, lo que incluye todos los archivos.

    Returns:
        tuple: 
        - (list): Lista de archivos filtrados encontrados.
        - (list): Lista de cadenas representando la estructura de directorios y archivos encontrados, incluyendo el peso de cada archivo en kB y el número de líneas de código.
    """
    archivos_encontrados = []
    estructura = []

    for raiz, _, archivos in os.walk(ruta):
        if debe_ignorar_directorio(raiz):
            continue

        nivel = calcular_nivel_indentacion(raiz, ruta)
        estructura.append(formatear_directorio(raiz, nivel))

        for archivo in archivos:
            archivo_completo = os.path.join(raiz, archivo)
            if archivo_valido(archivo_completo, extensiones_permitidas):
                archivos_encontrados.append(archivo_completo)
                estructura.append(formatear_archivo(archivo_completo, nivel + 1))

    return archivos_encontrados, estructura

def debe_ignorar_directorio(raiz):
    """Determina si un directorio debe ser ignorado."""
    return '.git' in raiz

def calcular_nivel_indentacion(raiz, ruta):
    """Calcula el nivel de indentación para la estructura."""
    return raiz.replace(ruta, '').count(os.sep)

def formatear_directorio(raiz, nivel):
    """Formatea el nombre del directorio con la indentación adecuada."""
    indentacion = ' ' * 4 * nivel
    return f"{indentacion}{os.path.basename(raiz)}/"

def archivo_valido(archivo_completo, extensiones_permitidas):
    """Determina si un archivo es válido basado en sus extensiones."""
    extension = os.path.splitext(archivo_completo)[1]
    return (not extensiones_permitidas or extension in extensiones_permitidas or
            os.path.basename(archivo_completo) in {'Pipfile', 'Pipfile.lock'})

def formatear_archivo(archivo_completo, nivel):
    """Formatea el archivo con su tamaño y número de líneas de código."""
    subindentacion = ' ' * 4 * nivel
    tamano_kb = obtener_tamano_archivo(archivo_completo)
    lineas_codigo = contar_lineas_codigo(archivo_completo, {'.py', '.ino', '.h'}, logger)
    espacio_vacio = ' ' * (50 - len(os.path.basename(archivo_completo)) - len(subindentacion))
    if lineas_codigo is None:
        return f"{subindentacion}{os.path.basename(archivo_completo)}{espacio_vacio}{tamano_kb:.2f}kB - N/A"
    else:
        return f"{subindentacion}{os.path.basename(archivo_completo)}{espacio_vacio}{tamano_kb:.2f}kB - {lineas_codigo:03d} líneas de código"

def obtener_tamano_archivo(archivo_completo):
    """Obtiene el tamaño del archivo en kilobytes."""
    return os.path.getsize(archivo_completo) / 1024
