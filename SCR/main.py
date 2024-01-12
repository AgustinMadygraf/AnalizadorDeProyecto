#main.py
import os
import sys
from importlib import metadata
from manipulacion_archivos import listar_archivos
from salida_datos import generar_archivo_salida
from utilidades_sistema import obtener_version_python, limpieza_pantalla
from interfaz_usuario import mostrar_opciones, elegir_modo
from logs.config_logger import configurar_logging
import subprocess

# Configuración del logger
logger = configurar_logging()

def obtener_ruta_default():
    ruta_script = obtener_ruta_script()
    archivo_default = os.path.join(ruta_script, '../config/config_path.txt')
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
        archivo_default = os.path.join(obtener_ruta_script(), '../config/config_path.txt')
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write(nueva_ruta)
    except Exception as e:
        logger.error(f"Error al guardar la nueva ruta por defecto: {e}")

def validar_ruta(ruta):
    return os.path.isdir(ruta) and os.access(ruta, os.R_OK)

def main():
    limpieza_pantalla()
    logger.info(f"Versión de Python en uso: {obtener_version_python()}")
    #crear_archivo_bat()
    modo_prompt = elegir_modo()
    ruta_anterior = None
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt']

    while True:
        ruta = ruta_anterior or obtener_ruta_default()
        if not validar_ruta(ruta):
            logger.error("La ruta proporcionada no es válida, no es accesible o no existe.")
            ruta_anterior = None
            exit()
        try:
            archivos, estructura = listar_archivos(ruta, extensiones)
            nombre_archivo_salida = generar_archivo_salida(ruta, archivos, estructura, modo_prompt, extensiones)
            if nombre_archivo_salida is None:
                logger.warning("No se generó ningún archivo.")
                ruta_anterior = None
                continue
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

def crear_archivo_bat():
    try:
        python_executable = sys.executable
        directorio_script = os.path.dirname(os.path.abspath(__file__))

        contenido_bat = (
            "@echo off\n"
            f"cd {directorio_script}\n"
            f"\"{python_executable}\" main.py\n"
            "pause\n"
        )

        ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat)
    except Exception as e:
        logger.error(f"Error al crear el archivo .bat: {e}")

if __name__ == "__main__":
    main()
