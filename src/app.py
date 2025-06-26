# src/app.py

import os
import time
import threading
from colorama import Fore, Style
from src.file_operations import listar_archivos
from src.domain.report_generator import ReportGenerator
from src.domain.file_manager import FileManager
from src.interfaces.file_manager_port import FileManagerPort
from src.infrastructure.file_manager_adapter import PythonFileManagerAdapter
from src.infrastructure.file_ops_adapter import FileOpsAdapter
from src.infrastructure.content_manager_adapter import ContentManagerAdapter
from src.infrastructure.clipboard_adapter import ClipboardAdapter
from src.utilities import obtener_version_python, limpieza_pantalla
from src.path_manager import seleccionar_ruta, validar_ruta, seleccionar_modo_operacion
from src.logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

def run_app(input_func=input):
    project_path = inicializar()
    # Wiring de dependencias según Clean Architecture
    file_manager_port = PythonFileManagerAdapter()
    file_ops_port = FileOpsAdapter()
    content_manager_port = ContentManagerAdapter()
    clipboard_port = ClipboardAdapter()
    report_generator = ReportGenerator(
        project_path,
        file_manager_port=file_manager_port,
        file_ops_port=file_ops_port,
        content_manager_port=content_manager_port,
        clipboard_port=clipboard_port,
        logger_port=logger
    )
    while True:
        if manejar_ruta_proyecto(project_path, report_generator, input_func):
            esperar_usuario(input_func)

def manejar_ruta_proyecto(project_path, report_generator, input_func):
    ruta = seleccionar_ruta(project_path, input_func)
    if not ruta or not validar_ruta(ruta):
        logger.error("La ruta proporcionada no es válida o no se puede acceder a ella.")
        return False

    incluir_todo = preguntar_incluir_todo_txt(input_func)
    inc_exc = "incluir" if incluir_todo else "excluir"
    logger.info(f'Se ha seleccionado la opción de {inc_exc} "todo.txt" para análisis.')

    modo_prompt = seleccionar_modo_operacion(input_func)
    procesar_archivos(ruta, modo_prompt, project_path, report_generator, incluir_todo)
    return True


def esperar_usuario(input_func=input):
    respuesta = input_func(f"{Fore.GREEN}\nPresiona Enter para reiniciar o escribe 'salir' para terminar...{Style.RESET_ALL}")
    if respuesta.strip().lower() in ("salir", "exit"):
        print(f"{Fore.YELLOW}Saliendo del AnalizadorDeProyecto. ¡Hasta luego!{Style.RESET_ALL}")
        exit(0)
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

    def mostrar_mensaje():
        nonlocal mostrar_todo
        for caracter in mensaje:
            if mostrar_todo:
                print(mensaje[mensaje.index(caracter):], end='', flush=True)
                break
            print(caracter, end='', flush=True)
            time.sleep(0.03)
        print()

    hilo_mensaje = threading.Thread(target=mostrar_mensaje)
    hilo_mensaje.start()

    input_func()
    mostrar_todo = True
    hilo_mensaje.join()

def procesar_archivos(ruta, modo_prompt, project_path, report_generator, incluir_todo):
    extensiones_permitidas = obtener_extensiones_permitidas()
    archivos = listar_archivos_en_ruta(ruta, extensiones_permitidas)
    generar_reporte(ruta, modo_prompt, project_path, report_generator, archivos, extensiones_permitidas, incluir_todo)

def obtener_extensiones_permitidas():
    return ['.html', '.css', '.php', '.js', '.py', '.json', '.sql', '.md', '.txt', '.ino', '.h']

def listar_archivos_en_ruta(ruta, extensiones_permitidas):
    archivos, _ = listar_archivos(ruta, extensiones_permitidas)
    return archivos

def generar_reporte(ruta, modo_prompt, project_path, report_generator, archivos, extensiones_permitidas, incluir_todo):
    report_generator.generar_archivo_salida(ruta, modo_prompt, extensiones_permitidas, project_path, incluir_todo)

def preguntar_incluir_todo_txt(input_func):
    respuesta = input_func(f"{Fore.GREEN}¿Desea incluir el análisis de 'todo.txt'? (S/N): {Style.RESET_ALL}").strip().lower()
    return respuesta == 's'

