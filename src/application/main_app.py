import os
from common.i18n import LANG
from domain.report_generator import ReportGenerator
from interfaces.file_manager_port import FileManagerPort
from interfaces.file_ops_port import FileOpsPort
from interfaces.content_manager_port import ContentManagerPort
from interfaces.clipboard_port import ClipboardPort
from interfaces.logger_port import LoggerPort
from interfaces.event_handler_port import IEventHandlerPort
from presentation.main_cli import bienvenida, esperar_usuario, limpieza_pantalla
from common.utilities import obtener_version_python
from application.path_manager import seleccionar_ruta, validar_ruta, seleccionar_modo_operacion
from colorama import Fore, Style

def inicializar(logger_port=None):
    limpieza_pantalla()
    bienvenida()  # <- UI
    if logger_port:
        logger_port.info(f"Versión de Python en uso: {obtener_version_python()}")
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.normpath(os.path.join(ruta_script, ".."))
    return project_path

# Nueva función: lógica de aplicación sin UI

def inicializar_sin_ui(logger_port=None):
    limpieza_pantalla()
    if logger_port:
        logger_port.info(f"Versión de Python en uso: {obtener_version_python()}")
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.normpath(os.path.join(ruta_script, ".."))
    return project_path


def run_app(
    file_manager_port: FileManagerPort,
    file_ops_port: FileOpsPort,
    content_manager_port: ContentManagerPort,
    clipboard_port: ClipboardPort,
    logger_port: LoggerPort,
    event_handler_port: IEventHandlerPort = None,
    input_func=input,
    mostrar_bienvenida=True,
):
    import sys
    if not sys.stdin.isatty():
        logger_port.warning(LANG.get('no_tty_warning', "[ADVERTENCIA] No se detecta terminal interactiva (TTY). El modo interactivo puede no funcionar correctamente."))
        logger_port.info(LANG.get('no_tty_suggestion', "Sugerencia: Use el modo batch con --no-interactive y los flags requeridos."))
        return
    if mostrar_bienvenida:
        project_path = inicializar(logger_port)
    else:
        project_path = inicializar_sin_ui(logger_port)
    report_generator = ReportGenerator(
        project_path,
        file_manager_port=file_manager_port,
        file_ops_port=file_ops_port,
        content_manager_port=content_manager_port,
        clipboard_port=clipboard_port,
        event_handler=event_handler_port
    )
    from presentation.main_cli import mostrar_error_ruta, mostrar_info_todo
    ui_callbacks = {
        'on_invalid_path': mostrar_error_ruta,
        'on_info': mostrar_info_todo
    }
    while True:
        try:
            if manejar_ruta_proyecto(project_path, report_generator, input_func, ui_callbacks=ui_callbacks, file_ops_port=file_ops_port, logger_port=logger_port, event_handler_port=event_handler_port):
                esperar_usuario(input_func)
        except KeyboardInterrupt:
            logger_port.info(f"\n{LANG.get('info_interrupted', '[INFO] Ejecución interrumpida por el usuario. Saliendo del programa...')}")
            break
        except Exception as e:
            logger_port.error(f"{LANG.get('error_unexpected', '[ERROR] Error inesperado: {e}').format(e=e)}")
            logger_port.info(LANG.get('suggestion', 'Sugerencia: Revise la ruta, permisos o reporte el error si persiste.'))
            break

def solicitar_ruta_valida(project_path, input_func, ui_callbacks=None, logger_port=None, event_handler_port=None, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        ruta = seleccionar_ruta(project_path, input_func)
        if ruta and validar_ruta(ruta):
            return ruta
        intentos += 1
        if event_handler_port:
            event_handler_port.publish('invalid_path', {'message': "La ruta proporcionada no es válida o no se puede acceder a ella."})
        if ui_callbacks and 'on_invalid_path' in ui_callbacks:
            ui_callbacks['on_invalid_path']()
        logger_port.error(f"Intento {intentos}/{max_intentos}. {LANG.get('try_again', 'Intente nuevamente. (Ctrl+C para salir)')}")
    logger_port.error(LANG.get('error_too_many_attempts', '[ERROR] Demasiados intentos fallidos. Saliendo del flujo de análisis.'))
    return None

def manejar_ruta_proyecto(project_path, report_generator, input_func, ui_callbacks=None, file_ops_port=None, logger_port=None, event_handler_port=None):
    ruta = solicitar_ruta_valida(project_path, input_func, ui_callbacks, logger_port, event_handler_port)
    if not ruta:
        return False
    incluir_todo = preguntar_incluir_todo_txt(input_func)
    inc_exc = "incluir" if incluir_todo else "excluir"
    if event_handler_port:
        event_handler_port.publish('todo_option_selected', {'option': inc_exc})
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
    modo_rapido = str(modo_prompt).strip().lower() in ["rapido", "resumen", "estructura"]
    if modo_rapido:
        report_generator.generar_archivo_salida_rapido(ruta, extensiones_permitidas)
    else:
        report_generator.generar_archivo_salida(ruta, modo_prompt, extensiones_permitidas, project_path, incluir_todo)

def preguntar_incluir_todo_txt(input_func):
    respuesta = input_func(LANG.get('prompt_include_todo', "¿Desea incluir el análisis de 'todo.txt'? (S/N): ")).strip().lower()
    return respuesta == 's' or respuesta == 'y'

# TODO: Refactorizar para que la lógica de aplicación y dominio no invoquen directamente logger_port.
# Propuesta: Emitir eventos o mensajes que la infraestructura pueda registrar.
# Ejemplo: return {'event': 'debug', 'message': ...} o usar un EventBus.
