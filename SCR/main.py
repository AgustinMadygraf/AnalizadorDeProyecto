#SCR/main.py
import os
from importlib import metadata
from manipulacion_archivos import listar_archivos
from salida_datos import generar_archivo_salida
from utilidades_sistema import obtener_version_python, limpieza_pantalla
from interfaz_usuario import mostrar_opciones, elegir_modo, solicitar_ruta
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

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

def guardar_nueva_ruta_default(nueva_ruta):
    """
    Guarda la nueva ruta por defecto en un archivo de configuración.

    Args:
        nueva_ruta (str): La nueva ruta a guardar como ruta por defecto.

    Esta función escribe la nueva ruta en un archivo 'path.txt' dentro de un directorio 'config'.
    Si el directorio 'config' no existe, la función intentará crearlo.
    """
    try:
        ruta_script = obtener_ruta_script()
        directorio_config = os.path.join(ruta_script, '../config')
        archivo_default = os.path.join(directorio_config, 'path.txt')

        # Crear directorio 'config' si no existe
        if not os.path.exists(directorio_config):
            os.makedirs(directorio_config)

        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write(nueva_ruta)

    except OSError as e:
        # Captura errores específicos relacionados con el sistema de archivos
        logger.error(f"Error al guardar la nueva ruta por defecto: {e}")
    except Exception as e:
        # Captura otros errores inesperados
        logger.error(f"Error inesperado al guardar la nueva ruta por defecto: {e}")

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

def control_de_flujo(ruta_proyecto):
    modo_prompt = elegir_modo()
    intentos = 0
    intentos_maximos = 5

    while True:
        ruta = obtener_ruta_default()  # Obtener la ruta por defecto

        if not validar_ruta(ruta) and intentos < intentos_maximos:
            ruta = solicitar_ruta()
            guardar_nueva_ruta_default(ruta)
            intentos += 1
        elif intentos >= intentos_maximos:
            logger.error("Número máximo de intentos alcanzado. Abortando.")
            break

        nombre_archivo_salida = procesar_archivos(ruta, modo_prompt, ruta_proyecto)

        opcion, nueva_ruta = mostrar_opciones(ruta)
        if opcion == 'S':
            break
        elif opcion == 'C':
            guardar_nueva_ruta_default(nueva_ruta)

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
    archivos, estructura = listar_archivos(ruta, extensiones)
    return generar_archivo_salida(ruta, archivos, estructura, modo_prompt, extensiones, ruta_proyecto)

def main():
    ruta_proyecto = inicializar()
    control_de_flujo(ruta_proyecto)

if __name__ == "__main__":
    main()
