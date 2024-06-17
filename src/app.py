#src/app.py
import os
import time
from datetime import datetime
import threading
import sys
import json
from colorama import Fore, Style
from importlib import metadata
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))  
from src.file_operations import listar_archivos
from src.report_generator import generar_archivo_salida
from utilities import obtener_version_python, limpieza_pantalla
from user_interface import  menu_0,menu_1
from logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def obtener_ruta_analisis(project_path):
    ruta_seleccionada = obtener_ruta_default()  # Esta ahora devuelve un diccionario
    if isinstance(ruta_seleccionada, dict):
        ruta_default = ruta_seleccionada['ruta']
    else:
        ruta_default = ruta_seleccionada  # En caso de que todavía soporte el formato antiguo

    logger.info(f"Directorio seleccionado: {ruta_default}\n")
    respuesta = input(f"{Fore.GREEN}¿Desea analizar el directorio? (S/N): {Style.RESET_ALL}").upper()
    print("")

    if respuesta == 'N':
        nueva_ruta = menu_0()  # Solicita al usuario una nueva ruta
        # Asegúrate de que guardar_nueva_ruta_default y cualquier otra función manejen correctamente el nuevo formato
        if nueva_ruta != ruta_default:
            guardar_nueva_ruta_default(nueva_ruta)
        return nueva_ruta

    return ruta_default

def run_app(): 
    project_path = inicializar()
    while True:
        ruta = obtener_ruta_analisis(project_path)
        if ruta and validar_ruta(ruta):
            modo_prompt = seleccionar_modo_operacion()
            procesar_archivos(ruta, modo_prompt, project_path)
            input(f"{Fore.GREEN}\nPresiona Enter para reiniciar...{Style.RESET_ALL}")
            limpieza_pantalla()
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
    project_path = os.path.normpath(os.path.join(ruta_script, ".."))
    return project_path

def bienvenida():
    mensaje = """Bienvenido al AnalizadorDeProyecto 🌟\nEste software es una herramienta avanzada diseñada para ayudarte a analizar, documentar y mejorar la estructura de tus proyectos de software...\n    ¡Esperamos que disfrutes utilizando esta herramienta y que te sea de gran ayuda en tus proyectos de software!"""

    mensaje = f"{mensaje}{Fore.GREEN} \n\n\nPresiona Enter para continuar...\n {Style.RESET_ALL}"

    mostrar_todo = False

    # Función que maneja la visualización del mensaje
    def mostrar_mensaje():
        nonlocal mostrar_todo
        for caracter in mensaje:
            if mostrar_todo:
                print(mensaje[mensaje.index(caracter):], end='', flush=True)
                break
            print(caracter, end='', flush=True)
            time.sleep(0.03)  
        print()  

    # Thread para mostrar el mensaje
    hilo_mensaje = threading.Thread(target=mostrar_mensaje)
    hilo_mensaje.start()

    # Espera a que el usuario presione Enter
    input()
    mostrar_todo = True
    hilo_mensaje.join()  # Espera a que el hilo termine

def guardar_nueva_ruta_default(nueva_ruta):
    archivo_default = 'config/path.json'
    try:
        # Cargar el archivo JSON existente o crear uno nuevo si no existe
        if os.path.exists(archivo_default):
            with open(archivo_default, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {"rutas": []}
        
        # Buscar la ruta en el archivo. Si existe, actualizar el timestamp
        ruta_existente = next((item for item in data["rutas"] if item["ruta"] == nueva_ruta), None)
        if ruta_existente:
            ruta_existente["ultimo_acceso"] = datetime.now().isoformat()
        else:
            # Añadir la nueva ruta al principio de la lista con el timestamp actual
            data["rutas"].insert(0, {"ruta": nueva_ruta, "ultimo_acceso": datetime.now().isoformat()})
        
        # Guardar el archivo JSON actualizado
        with open(archivo_default, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        
        logger.info(f"Nueva ruta por defecto guardada: {nueva_ruta}")
    except Exception as e:
        logger.error(f"Error al guardar la nueva ruta por defecto: {e}")

def obtener_ruta_default():
    archivo_default = 'config/path.json'
    if not os.path.exists(archivo_default):
        logger.info(f"El archivo {archivo_default} no existe. Creando uno nuevo.")
        crear_archivo_path_json()  # Llamada a la nueva función para crear el archivo
    try:
        with open(archivo_default, 'r', encoding='utf-8') as file:
            data = json.load(file)
            rutas = data.get('rutas', [])
        
        if not rutas:
            nueva_ruta = input("No se encontraron rutas guardadas. Por favor, introduzca una nueva ruta: ").strip()
            guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta

        # Presentar las rutas de manera más amigable
        for i, ruta_info in enumerate(rutas, start=1):
            ruta = ruta_info['ruta']
            ultimo_acceso = ruta_info['ultimo_acceso']
            # Formatea y muestra cada ruta y su último acceso de manera clara
            logger.info(f"{i}. Ruta: {ruta} - Último acceso: {ultimo_acceso}")

        # Opción para introducir una nueva ruta
        logger.info(f"{len(rutas)+1}. Introducir una nueva ruta")
        print("")

        eleccion = input(f"{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}").strip()        # Procesamiento de la elección del usuario
        if not eleccion:
            return rutas[0]['ruta']
        elif eleccion.isdigit() and 1 <= int(eleccion) <= len(rutas):
            return rutas[int(eleccion)-1]['ruta']
        elif eleccion == str(len(rutas) + 1):
            nueva_ruta = input("Introduzca la nueva ruta: ").strip()
            guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta
        else:
            logger.warning("Opción no válida.")
            return obtener_ruta_default()
    except Exception as e:
        logger.error(f"Ocurrió un error: {e}")
    except FileNotFoundError:
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
    # Asegurarse de que 'ruta' no sea None y sea una cadena no vacía
    if not ruta or not isinstance(ruta, str):
        logger.error(f"Validación de ruta fallida, la ruta proporcionada es inválida: '{ruta}'")
        return False

    # Verifica si la ruta es un directorio
    es_directorio = os.path.isdir(ruta)

    # Verifica si el directorio es accesible para lectura
    es_accesible = os.access(ruta, os.R_OK)

    if not es_directorio or not es_accesible:
        logger.error(f"La ruta no es un directorio o no es accesible para lectura: '{ruta}'")
        return False

    return True

def procesar_archivos(ruta, modo_prompt, ruta_archivos):
    """
    Procesa los archivos en una ruta de proyecto dada.

    Args:
        ruta (str): Ruta a los archivos a procesar.
        modo_prompt (str): Modo seleccionado para el procesamiento de archivos.
        project_path (str): Ruta al directorio del proyecto.

    Realiza operaciones de archivo basadas en el modo seleccionado y guarda la salida.
    """
    extensiones = ['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt']
    listar_archivos(ruta, extensiones)
    return generar_archivo_salida(ruta, modo_prompt, extensiones, ruta_archivos)

def crear_archivo_path_json():
    ruta_directorio = 'config'
    archivo_default = os.path.join(ruta_directorio, 'path.json')

    # Obtener la ruta absoluta del directorio del proyecto
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Obtener la fecha y hora actuales en formato ISO
    ultimo_acceso = datetime.now().isoformat()

    # Estructura inicial con la ruta del proyecto y la fecha/hora actuales
    contenido_inicial = {
        "rutas": [
            {
                "ruta": project_path,
                "ultimo_acceso": ultimo_acceso
            }
        ]
    }

    # Crear el directorio `config` si no existe
    if not os.path.exists(ruta_directorio):
        os.makedirs(ruta_directorio)
        logger.info(f"Directorio {ruta_directorio} creado.")

    # Crear y escribir en el archivo `path.json`
    try:
        with open(archivo_default, 'w', encoding='utf-8') as file:
            json.dump(contenido_inicial, file, indent=4)
        logger.info(f"Archivo {archivo_default} creado con éxito. Ruta del proyecto y fecha/hora actuales añadidas.")
    except Exception as e:
        logger.error(f"No se pudo crear el archivo {archivo_default}: {e}")

