#SCR/Principal.py
import os
import time
from importlib import metadata
from ManiArch import listar_archivos
from SalidDatos import generar_archivo_salida
from UtilSist import obtener_version_python, limpieza_pantalla
from InterfazHM import  menu_0,menu_1, menu_2,menu_3 #, menu_4
from logs.config_logger import configurar_logging


# Configuración del logger
logger = configurar_logging()

def obtener_ruta_analisis():
    """
    Obtiene la ruta a analizar, ya sea por defecto o proporcionada por el usuario.
    """
    respuesta = input("¿Desea analizar el directorio por defecto? (S/N): ").upper()
    if respuesta == 'N':
        return menu_0()  # Solicita al usuario una nueva ruta
    return obtener_ruta_default()

def main():
    ruta_proyecto = inicializar()
    ruta = obtener_ruta_analisis()
    if ruta and validar_ruta(ruta):
        modo_prompt = seleccionar_modo_operacion()
        procesar_archivos(ruta, modo_prompt, ruta_proyecto)
        realizar_pasos_adicionales(modo_prompt, ruta)

def seleccionar_modo_operacion():
    """
    Permite al usuario seleccionar el modo de operación y devuelve el prompt correspondiente.
    """
    return menu_1()

def realizar_pasos_adicionales(modo_prompt, ruta):
    """
    Realiza pasos adicionales basados en el modo de operación seleccionado.
    """
    menu_2(modo_prompt, ruta)
    menu_3(modo_prompt, ruta)

def inicializar():
    """
    Inicializa el entorno del script.

    Limpia la pantalla, muestra la versión de Python en uso y calcula la ruta del proyecto
    basándose en la ubicación del script actual. Imprime y devuelve la ruta del proyecto.

    Returns:
        str: La ruta del proyecto.
    """
    limpieza_pantalla()
    logger.debug(f"Versión de Python en uso: {obtener_version_python()}")
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_proyecto = os.path.normpath(os.path.join(ruta_script, ".."))
    return ruta_proyecto

def obtener_ruta_default():
    """
    Obtiene la ruta por defecto desde un archivo de configuración.

    Intenta leer un archivo 'path.txt' ubicado en el directorio 'config' relativo al script actual.
    Si el archivo no existe, lo crea con un valor predeterminado y luego devuelve ese valor.

    Returns:
        str: La ruta por defecto leída del archivo o un valor predeterminado si el archivo no existe.
    """
    ruta_script = obtener_ruta_script()
    archivo_default = os.path.join(ruta_script, '../config/path.txt')

    # Asegurarse de que el directorio 'config' exista
    os.makedirs(os.path.dirname(archivo_default), exist_ok=True)

    try:
        with open(archivo_default, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        # Especifica un valor más significativo o deja en blanco según tus necesidades
        valor_por_defecto = "Especifica_tu_ruta_aquí"
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write(valor_por_defecto)
        return valor_por_defecto

def obtener_ruta_script():
    """
    Obtiene la ruta del directorio del script actual.

    Utiliza la variable mágica '__file__' para obtener la ruta completa del script en ejecución
    y luego extrae el directorio que lo contiene. Es útil para construir rutas relativas a la
    ubicación del script, independientemente del directorio de trabajo actual.

    Returns:
        str: Ruta del directorio donde se encuentra el script actual.
    """
    return os.path.dirname(os.path.abspath(__file__))

def validar_ruta(ruta):
    """
    Verifica si la ruta proporcionada es un directorio y si es accesible para lectura.

    Args:
        ruta (str): La ruta del directorio a validar.

    Returns:
        bool: True si la ruta es un directorio y es accesible para lectura, False en caso contrario.
    """
    # Verifica si la ruta es un directorio
    es_directorio = os.path.isdir(ruta)

    # Verifica si el directorio es accesible para lectura
    es_accesible = os.access(ruta, os.R_OK)

    return es_directorio and es_accesible

def procesar_archivos(ruta, modo_prompt, ruta_proyecto):
    """
    Procesa los archivos en una ruta de proyecto dada.

    Args:
        ruta (str): Ruta a los archivos a procesar.
        modo_prompt (str): Modo seleccionado para el procesamiento de archivos.
        ruta_proyecto (str): Ruta al directorio del proyecto.

    Realiza operaciones de archivo basadas en el modo seleccionado y guarda la salida.
    """
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt']
    listar_archivos(ruta, extensiones)
    return generar_archivo_salida(ruta, modo_prompt, extensiones, ruta_proyecto)



if __name__ == "__main__":
    main()
