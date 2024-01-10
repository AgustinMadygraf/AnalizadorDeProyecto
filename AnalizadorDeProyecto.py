# C:\AppServ\www\AnalizadorDeProyecto\AnalizadorDeProyecto.py

import os
import sys
from importlib import metadata
from gestion_archivos import listar_archivos, generar_archivo_salida
from utilidades_sistema import verificar_e_instalar_librerias, obtener_version_python, limpieza_pantalla
from interfaz_usuario import mostrar_opciones
from interfaz_usuario import elegir_modo
import logging

logging.basicConfig(filename='analizador.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_ruta_default():
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        archivo_default = os.path.join(ruta_script, 'default.txt')
        if not os.path.exists(archivo_default):
            with open(archivo_default, 'w', encoding='utf-8') as file:
                file.write("Contenido por defecto o dejar esta línea en blanco")
        with open(archivo_default, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError as e:
        logging.error(f"Archivo default.txt no encontrado: {e}")
        return None

def guardar_nueva_ruta_default(nueva_ruta):
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        archivo_default = os.path.join(ruta_script, 'default.txt')
        print(f"Intentando escribir en: {archivo_default}")  # Agregar para depuración
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write(nueva_ruta)
        print("Ruta guardada con éxito.")  # Agregar para depuración
    except Exception as e:
        print(f"Error al guardar la nueva ruta por defecto: {e}")

def validar_ruta(ruta):
    return os.path.isdir(ruta) and os.access(ruta, os.R_OK)

def main():
    limpieza_pantalla()
    logging.info(f"Versión de Python en uso: {obtener_version_python()}")
    librerias_necesarias = ['pyperclip', 'datetime', 'importlib']
    verificar_e_instalar_librerias(librerias_necesarias)

    modo_prompt = elegir_modo()  # Llama a la función para elegir el modo

    ruta_anterior = None
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.me', '.txt']
    while True:
        ruta = ruta_anterior or obtener_ruta_default()
        if not validar_ruta(ruta):
            print("La ruta proporcionada no es válida, no es accesible o no existe.")
            ruta_anterior = None
            continue
        try:
            archivos, estructura = listar_archivos(ruta, extensiones)
            nombre_archivo_salida = generar_archivo_salida(ruta, archivos, estructura,modo_prompt)
            if nombre_archivo_salida is None:
                logging.warning("No se generó ningún archivo.")
                ruta_anterior = None
                continue
        except Exception as e:
            logging.error(f"Error al procesar la ruta: {e}")
            ruta_anterior = None
            continue

        opcion, nueva_ruta = mostrar_opciones(ruta)
        if opcion == 'S':
            break
        elif opcion == 'C':
            guardar_nueva_ruta_default(nueva_ruta)  # Guardar la nueva ruta en default.txt
            ruta_anterior = nueva_ruta  # Actualizar la ruta anterior con la nueva ruta
        else:
            ruta_anterior = ruta

def crear_archivo_bat():
    try:
        python_executable = sys.executable  # Ubicación del ejecutable de Python
        directorio_script = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
        ruta_script = os.path.join(directorio_script, 'AnalizadorDeProyecto.py')  # Ruta completa del script

        contenido_bat = f'@echo off\n"{python_executable}" "{ruta_script}"\npause\n'

        ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat)

        print(f'Archivo .bat creado en: {ruta_archivo_bat}')
    except Exception as e:
        print(f"Error al crear el archivo .bat: {e}")

if __name__ == "__main__":
    main()
