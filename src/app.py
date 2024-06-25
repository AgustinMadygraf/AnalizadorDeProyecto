#AnalizadorDeProyecto/src/app.py
import os
import time
import threading
from colorama import Fore, Style
from src.file_operations import listar_archivos
from src.report_generator import generar_archivo_salida
from src.utilities import obtener_version_python, limpieza_pantalla
from src.path_manager import seleccionar_ruta, validar_ruta, seleccionar_modo_operacion
from src.logs.config_logger import configurar_logging

# Configuración del logger
logger = configurar_logging()

def run_app(input_func=input):
    project_path = inicializar()
    while True:
        if manejar_ruta_proyecto(project_path, input_func):
            esperar_usuario(input_func)

def manejar_ruta_proyecto(project_path, input_func):
    ruta = seleccionar_ruta(project_path, input_func)
    if ruta and validar_ruta(ruta):
        modo_prompt = seleccionar_modo_operacion(input_func)
        procesar_archivos(ruta, modo_prompt, project_path)
        return True
    else:
        logger.error("La ruta proporcionada no es válida o no se puede acceder a ella.")
        return False


def esperar_usuario(input_func=input):
    input_func(f"{Fore.GREEN}\nPresiona Enter para reiniciar...{Style.RESET_ALL}")
    limpieza_pantalla()

def inicializar():
    limpieza_pantalla()
    bienvenida()
    logger.debug(f"Versión de Python en uso: {obtener_version_python()}")
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.normpath(os.path.join(ruta_script, ".."))
    return project_path


def bienvenida(input_func=input):
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
    input_func()
    mostrar_todo = True
    hilo_mensaje.join()  # Espera a que el hilo termine





def procesar_archivos(ruta, modo_prompt, ruta_archivos):
    """
    Procesa los archivos en una ruta de proyecto dada.

    Args:
        ruta (str): Ruta a los archivos a procesar.
        modo_prompt (str): Modo seleccionado para el procesamiento de archivos.
        project_path (str): Ruta al directorio del proyecto.

    Realiza operaciones de archivo basadas en el modo seleccionado y guarda la salida.
    """
    extensiones_permitidas= ['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt', '.ino','.h' ]
    listar_archivos(ruta, extensiones_permitidas)
    return generar_archivo_salida(ruta, modo_prompt, extensiones_permitidas, ruta_archivos)
