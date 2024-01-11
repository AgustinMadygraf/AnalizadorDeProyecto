# C:\AppServ\www\AnalizadorDeProyecto\AnalizadorDeProyecto.py

import os
import sys
from importlib import metadata
from gestion_archivos import listar_archivos, generar_archivo_salida
from utilidades_sistema import verificar_e_instalar_librerias, obtener_version_python, limpieza_pantalla
from interfaz_usuario import mostrar_opciones
from interfaz_usuario import elegir_modo
import logging

logging.basicConfig(filename='logs/analizador.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def obtener_ruta_default():
    ruta_script = obtener_ruta_script()  # Nueva función para obtener la ruta
    archivo_default = os.path.join(ruta_script, 'config_path.txt')
    try:
        with open(archivo_default, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write("Contenido por defecto o dejar esta línea en blanco")
            return "Contenido por defecto o dejar esta línea en blanco"

def obtener_ruta_script():
    """
    Obtiene la ruta absoluta del directorio donde se encuentra el script actual.

    Retorna:
        str: La ruta del directorio del script actual.
    """
    return os.path.dirname(os.path.abspath(__file__))

def guardar_nueva_ruta_default(nueva_ruta):
    try:
        archivo_default = os.path.join(obtener_ruta_script(), 'config_path.txt')
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
    crear_archivo_bat()
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
            guardar_nueva_ruta_default(nueva_ruta)  # Guardar la nueva ruta en config_path.txt
            ruta_anterior = nueva_ruta  # Actualizar la ruta anterior con la nueva ruta
        else:
            ruta_anterior = ruta

def crear_archivo_bat():
    try:
        python_executable = sys.executable  # Ubicación del ejecutable de Python
        directorio_script = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual

        # Modificación aquí: Agregar 'cd' para cambiar al directorio del script
        contenido_bat = (
            "@echo off\n"
            f"cd {directorio_script}\n"  # Cambia al directorio del script
            f"\"{python_executable}\" main.py\n"  # Ejecuta main.py
            "pause\n"
        )

        ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat)

        print(f'Archivo .bat creado en: {ruta_archivo_bat}')
    except Exception as e:
        print(f"Error al crear el archivo .bat: {e}")

if __name__ == "__main__":
    main()
