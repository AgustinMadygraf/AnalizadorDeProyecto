# AnalizadorDeProyecto.py

import os
import sys
import subprocess
from importlib import metadata
from gestion_archivos import listar_archivos, escribir_contenido_archivo, generar_archivo_salida
from utilidades_sistema import verificar_e_instalar_librerias, obtener_version_python, obtener_librerias_pip
from interfaz_usuario import solicitar_ruta, mostrar_opciones

def obtener_ruta_default():
    try:
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        archivo_default = os.path.join(ruta_script, 'default.txt')
        if not os.path.exists(archivo_default):
            with open(archivo_default, 'w', encoding='utf-8') as file:
                file.write("Contenido por defecto o dejar esta línea en blanco")
        with open(archivo_default, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error al obtener la ruta por defecto: {e}")
        return None

def validar_ruta(ruta):
    return os.path.isdir(ruta) and os.access(ruta, os.R_OK)

def main():
    ruta_anterior = None
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.me']
    while True:
        ruta = ruta_anterior or obtener_ruta_default()
        if not validar_ruta(ruta):
            print("La ruta proporcionada no es válida, no es accesible o no existe.")
            ruta_anterior = None
            continue
        try:
            archivos, estructura = listar_archivos(ruta, extensiones)
            nombre_archivo_salida = generar_archivo_salida(ruta, archivos, estructura)
            if nombre_archivo_salida is None:
                print("No se generó ningún archivo.")
                ruta_anterior = None
                continue
        except Exception as e:
            print(f"Error al procesar la ruta: {e}")
            ruta_anterior = None
            continue

        opcion, nueva_ruta = mostrar_opciones(ruta)
        if opcion == 'S':
            break
        elif opcion == 'C':
            ruta_anterior = nueva_ruta
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
