import os
from src.domain.report_generator import ReportGenerator
from src.interfaces.logger_port import LoggerPort
from src.interfaces.content_manager_port import ContentManagerPort
from src.interfaces.file_manager_port import FileManagerPort
from src.interfaces.clipboard_port import ClipboardPort
from src.presentation.main_cli import bienvenida, esperar_usuario
from src.common.utilities import obtener_version_python
from src.infrastructure.utils.screen_utils import limpieza_pantalla
from src.application.path_manager import seleccionar_ruta, validar_ruta, seleccionar_modo_operacion
from src.logs.config_logger import LoggerConfigurator
from colorama import Fore, Style

logger = LoggerConfigurator().get_logger()

def inicializar():
    limpieza_pantalla()
    bienvenida()  # <- UI
    logger.debug("Versión de Python en uso: %s", obtener_version_python())
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.normpath(os.path.join(ruta_script, ".."))
    return project_path

# Nueva función: lógica de aplicación sin UI

def inicializar_sin_ui():
    limpieza_pantalla()
    logger.debug("Versión de Python en uso: %s", obtener_version_python())
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.normpath(os.path.join(ruta_script, ".."))
    return project_path

def run_app(
    file_manager_port: FileManagerPort,
    file_ops_port,  # Asumir interfaz si existe
    content_manager_port: ContentManagerPort,
    clipboard_port: ClipboardPort,
    logger_port: LoggerPort,
    input_func=input,
    mostrar_bienvenida=True
):
    from src.presentation.main_cli import mostrar_error_ruta, mostrar_info_todo
    ui_callbacks = {
        'on_invalid_path': mostrar_error_ruta,
        'on_info': mostrar_info_todo
    }
    if mostrar_bienvenida:
        project_path = inicializar()
    else:
        project_path = inicializar_sin_ui()
    report_generator = ReportGenerator(
        project_path,
        file_manager_port=file_manager_port,
        file_ops_port=file_ops_port,
        content_manager_port=content_manager_port,
        clipboard_port=clipboard_port,
        logger_port=logger_port
    )
    while True:
        if manejar_ruta_proyecto(project_path, report_generator, input_func, ui_callbacks=ui_callbacks, file_ops_port=file_ops_port):
            esperar_usuario(input_func)

def manejar_ruta_proyecto(project_path, report_generator, input_func, ui_callbacks=None, file_ops_port=None):
    # ui_callbacks: {'on_invalid_path': func, 'on_info': func}
    ruta = seleccionar_ruta(project_path, input_func)
    if not ruta or not validar_ruta(ruta):
        logger.error("La ruta proporcionada no es válida o no se puede acceder a ella.")
        if ui_callbacks and 'on_invalid_path' in ui_callbacks:
            ui_callbacks['on_invalid_path']()
        return False
    incluir_todo = preguntar_incluir_todo_txt(input_func)
    inc_exc = "incluir" if incluir_todo else "excluir"
    logger.info('Se ha seleccionado la opción de %s "todo.txt" para análisis.', inc_exc)
    if ui_callbacks and 'on_info' in ui_callbacks:
        ui_callbacks['on_info'](inc_exc)
    modo_prompt = seleccionar_modo_operacion(input_func)
    procesar_archivos(ruta, modo_prompt, project_path, report_generator, incluir_todo, file_ops_port)
    return True

def procesar_archivos(ruta, modo_prompt, project_path, report_generator, incluir_todo, file_ops_port):
    extensiones_permitidas = obtener_extensiones_permitidas()
    archivos = listar_archivos_en_ruta(ruta, extensiones_permitidas, file_ops_port)
    generar_reporte(ruta, modo_prompt, project_path, report_generator, extensiones_permitidas, incluir_todo)

def obtener_extensiones_permitidas():
    return ['.html', '.css', '.php', '.js', '.py', '.json', '.sql', '.md', '.txt', '.ino', '.h']

def listar_archivos_en_ruta(ruta, extensiones_permitidas, file_ops_port):
    archivos, _ = file_ops_port.listar_archivos(ruta, extensiones_permitidas)
    return archivos

def generar_reporte(ruta, modo_prompt, project_path, report_generator, extensiones_permitidas, incluir_todo):
    report_generator.generar_archivo_salida(ruta, modo_prompt, extensiones_permitidas, project_path, incluir_todo)

def preguntar_incluir_todo_txt(input_func):
    respuesta = input_func(f"{Fore.GREEN}¿Desea incluir el análisis de 'todo.txt'? (S/N): {Style.RESET_ALL}").strip().lower()
    return respuesta == 's'
