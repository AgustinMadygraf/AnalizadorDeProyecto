#SCR/main.py
import os
from importlib import metadata
from manipulacion_archivos import listar_archivos
from salida_datos import generar_archivo_salida
from utilidades_sistema import obtener_version_python, limpieza_pantalla
from interfaz_usuario import mostrar_opciones, elegir_modo, solicitar_ruta
from logs.config_logger import configurar_logging
import subprocess
import datetime


# Configuración del logger
logger = configurar_logging()

def obtener_ruta_default():
    ruta_script = obtener_ruta_script()
    archivo_default = os.path.join(ruta_script, '../config/path.txt')
    try:
        with open(archivo_default, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write("Contenido por defecto o dejar esta línea en blanco")
            return "Contenido por defecto o dejar esta línea en blanco"

def obtener_ruta_script():
    return os.path.dirname(os.path.abspath(__file__))

def guardar_nueva_ruta_default(nueva_ruta):
    try:
        archivo_default = os.path.join(obtener_ruta_script(), '../config/path.txt')
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write(nueva_ruta)
    except Exception as e:
        logger.error(f"Error al guardar la nueva ruta por defecto: {e}")

def validar_ruta(ruta):
    return os.path.isdir(ruta) and os.access(ruta, os.R_OK)



def main():
    limpieza_pantalla()
    logger.info(f"Versión de Python en uso: {obtener_version_python()}")
    modo_prompt = elegir_modo()
    ruta_anterior = None
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt']

    while True:
        ruta = ruta_anterior or obtener_ruta_default()
        if not validar_ruta(ruta):
            logger.error("La ruta proporcionada no es válida, no es accesible o no existe.")
            ruta = solicitar_ruta()  # Pide al usuario que introduzca una ruta
            guardar_nueva_ruta_default(ruta)  # Guarda la nueva ruta en path.txt
            ruta_anterior = ruta

        try:
            archivos, estructura = listar_archivos(ruta, extensiones)
            nombre_archivo_salida = generar_archivo_salida(ruta, archivos, estructura, modo_prompt, extensiones)
            if nombre_archivo_salida is None:
                logger.warning("No se generó ningún archivo.")
                ruta_anterior = None
            fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Fecha y hora de generación: {fecha_hora_actual}")
        except Exception as e:
            logger.error(f"Error al procesar la ruta: {e}")
            ruta_anterior = None
            continue

        opcion, nueva_ruta = mostrar_opciones(ruta)
        if opcion == 'S':
            break
        elif opcion == 'C':
            guardar_nueva_ruta_default(nueva_ruta)
            ruta_anterior = nueva_ruta
        else:
            ruta_anterior = ruta

if __name__ == "__main__":
    main()
