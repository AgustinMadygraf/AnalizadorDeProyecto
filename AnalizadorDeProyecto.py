import os
import sys
import subprocess
from importlib import metadata
from gestion_archivos import listar_archivos, escribir_contenido_archivo, generar_archivo_salida
from utilidades_sistema import verificar_e_instalar_librerias, obtener_version_python, obtener_librerias_pip
from interfaz_usuario import solicitar_ruta, mostrar_opciones  

# Obtener ruta del archivo default
def obtener_ruta_default():
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    archivo_default = os.path.join(ruta_script, 'default.txt')
    if not os.path.exists(archivo_default):
        with open(archivo_default, 'w', encoding='utf-8') as file:
            file.write("Contenido por defecto o dejar esta línea en blanco")
    with open(archivo_default, 'r', encoding='utf-8') as file:
        return file.read().strip()

# Solicitar ruta al usuario
def solicitar_ruta():
    return input("Ingrese la ruta de la carpeta: ")

def main():
    ruta_anterior = None
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.me']
    while True:
        ruta = ruta_anterior or obtener_ruta_default()
        if not os.path.isdir(ruta):
            print("La ruta proporcionada no es válida o no es accesible.")
            ruta_anterior = None
            continue
        nombre_archivo_salida = generar_archivo_salida(ruta, *listar_archivos(ruta, extensiones))
        if nombre_archivo_salida is None:
            print("No se generó ningún archivo.")
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
    python_executable = sys.executable  # Ubicación del ejecutable de Python
    directorio_script = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
    ruta_script = os.path.join(directorio_script, 'AnalizadorDeProyecto.py')  # Ruta completa del script

    contenido_bat = f'@echo off\n"{python_executable}" "{ruta_script}"\npause\n'

    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
    with open(ruta_archivo_bat, 'w') as archivo_bat:
        archivo_bat.write(contenido_bat)

    print(f'Archivo .bat creado en: {ruta_archivo_bat}')

# Llamar a la función para crear el archivo .bat
crear_archivo_bat()

if __name__ == "__main__":
    main()
