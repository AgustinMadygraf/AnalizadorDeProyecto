#src/main.py
import os
import time
import threading
import sys
import json
from importlib import metadata
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))  
from file_operations import listar_archivos
from src.output_generation import generar_archivo_salida
from utilities import obtener_version_python, limpieza_pantalla
from user_interface import  menu_0,menu_1
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def obtener_ruta_analisis(ruta_proyecto):
    ruta_default = obtener_ruta_default()
    logger.info(f"Directorio por defecto: {ruta_default}")
    respuesta = input("¿Desea analizar el directorio? (S/N): ").upper()
    if respuesta == 'N':
        nueva_ruta = menu_0()  # Solicita al usuario una nueva ruta
        if nueva_ruta != ruta_default:
            guardar_nueva_ruta_default(nueva_ruta)
        return nueva_ruta
    return ruta_default

def main():
    ruta_proyecto = inicializar()
    while True:
        ruta = obtener_ruta_analisis(ruta_proyecto)
        print("\n\nruta: ",ruta,"\n\n")
        if ruta and validar_ruta(ruta):
            modo_prompt = seleccionar_modo_operacion()
            procesar_archivos(ruta, modo_prompt, ruta_proyecto)
            print("El archivo de salida ha sido generado con éxito.\n\n")
        else:
            logger.error("La ruta proporcionada no es válida o no se puede acceder a ella.")

def seleccionar_modo_operacion():
    """
    Permite al usuario seleccionar el modo de operación y devuelve el prompt correspondiente.
    """
    return menu_1()

def inicializar():
    """
    Inicializa el entorno del script.

    Limpia la pantalla, muestra la versión de Python en uso y calcula la ruta del proyecto
    basándose en la ubicación del script actual. Imprime y devuelve la ruta del proyecto.

    Returns:
        str: La ruta del proyecto.
    """
    limpieza_pantalla()
    bienvenida()
    logger.debug(f"Versión de Python en uso: {obtener_version_python()}")
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    ruta_proyecto = os.path.normpath(os.path.join(ruta_script, ".."))
    return ruta_proyecto

def bienvenida():
    mensaje = """Bienvenido al AnalizadorDeProyecto 🌟\nEste software es una herramienta avanzada diseñada para ayudarte a analizar, documentar y mejorar la estructura de tus proyectos de software...\n    ¡Esperamos que disfrutes utilizando esta herramienta y que te sea de gran ayuda en tus proyectos de software!\n\n\nPresiona Enter para continuar...\n"""

    mostrar_todo = False

    # Función que maneja la visualización del mensaje
    def mostrar_mensaje():
        nonlocal mostrar_todo
        for caracter in mensaje:
            if mostrar_todo:
                print(mensaje[mensaje.index(caracter):], end='', flush=True)
                break
            print(caracter, end='', flush=True)
            time.sleep(0.05)  # Ajusta este valor según sea necesario
        print()  # Asegura una nueva línea después del mensaje

    # Thread para mostrar el mensaje
    hilo_mensaje = threading.Thread(target=mostrar_mensaje)
    hilo_mensaje.start()

    # Espera a que el usuario presione Enter
    input()
    mostrar_todo = True
    hilo_mensaje.join()  # Espera a que el hilo termine

    # Avanza a la siguiente etapa después de la segunda pulsación de Enter

def guardar_nueva_ruta_default(nueva_ruta):
    archivo_default = 'config/path.json'
    try:
        # Cargar el archivo JSON existente o crear uno nuevo si no existe
        if os.path.exists(archivo_default):
            with open(archivo_default, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {"rutas": []}
        
        # Añadir la nueva ruta al principio de la lista (última usada)
        if nueva_ruta not in data["rutas"]:
            data["rutas"].insert(0, nueva_ruta)
        else:
            # Mover la ruta al principio si ya existe
            data["rutas"].insert(0, data["rutas"].pop(data["rutas"].index(nueva_ruta)))
        
        # Guardar el archivo JSON actualizado
        with open(archivo_default, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        print(f"Nueva ruta por defecto guardada: {nueva_ruta}")
    except Exception as e:
        print(f"Error al guardar la nueva ruta por defecto: {e}")


def obtener_ruta_default():
    archivo_default = 'config/path.json'
    try:
        with open(archivo_default, 'r', encoding='utf-8') as file:
            data = json.load(file)
            rutas = data.get('rutas', [])
            
        # Si no hay rutas guardadas, pedir al usuario que introduzca una
        if not rutas:
            nueva_ruta = input("No se encontraron rutas guardadas. Por favor, introduzca una nueva ruta: ").strip()
            guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta
        
        # Mostrar rutas existentes y permitir elegir una
        print("Seleccione una ruta:")
        for i, ruta in enumerate(rutas, start=1):
            print(f"{i}. {ruta}")
        print(f"{len(rutas)+1}. Introducir una nueva ruta")
        
        eleccion = input("Seleccione una opción: ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(rutas):
            # Elegir una ruta existente
            return rutas[int(eleccion)-1]
        elif eleccion == str(len(rutas) + 1):
            # Añadir una nueva ruta
            nueva_ruta = input("Introduzca la nueva ruta: ").strip()
            guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta
        else:
            print("Opción no válida.")
            return obtener_ruta_default()
            
    except FileNotFoundError:
        # Si no existe el archivo, pedir una ruta nueva
        nueva_ruta = input("Por favor, introduzca una nueva ruta: ").strip()
        guardar_nueva_ruta_default(nueva_ruta)
        return nueva_ruta

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

def procesar_archivos(ruta, modo_prompt, ruta_archivos):
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
    return generar_archivo_salida(ruta, modo_prompt, extensiones, ruta_archivos)


if __name__ == "__main__":
    main()
