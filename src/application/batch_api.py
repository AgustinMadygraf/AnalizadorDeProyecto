"""
API de alto nivel para uso batch/no interactivo del AnalizadorDeProyecto.
Permite invocar análisis y generación de reportes desde CLI o scripts.
"""
# pylint: disable=import-error
from src.domain.report_generator import ReportGenerator
from src.interfaces.file_manager_port import FileManagerPort
from src.interfaces.file_ops_port import FileOpsPort
from src.interfaces.content_manager_port import ContentManagerPort
from src.interfaces.clipboard_port import ClipboardPort
from src.interfaces.logger_port import LoggerPort
from src.interfaces.event_handler_port import IEventHandlerPort
from src.domain.file_manager import FileManager

# TODO: Revisar posible código muerto (vulture): función 'analizar_y_generar_reporte' reportada como sin uso

def analizar_y_generar_reporte(
    ruta: str,
    modo_prompt: str,
    project_path: str,
    incluir_todo: bool,
    file_manager_port: FileManagerPort,
    file_ops_port: FileOpsPort,
    content_manager_port: ContentManagerPort,
    clipboard_port: ClipboardPort,
    logger_port: LoggerPort = None,
    event_handler_port: IEventHandlerPort = None,
    rapido: bool = False,
    handler_factory=None  # Nuevo parámetro opcional
):
    eventos = []
    eventos.append({'type': 'log', 'level': 'info', 'message': f"[BATCH] Iniciando análisis en: {ruta}"})
    # Crear FileManager con handler_factory y logger
    file_manager = FileManager(project_path, logger_port, handler_factory) if handler_factory else file_manager_port
    report_generator = ReportGenerator(
        project_path,
        file_manager_port=file_manager,
        file_ops_port=file_ops_port,
        content_manager_port=content_manager_port,
        clipboard_port=clipboard_port,
        event_handler=event_handler_port
    )
    extensiones_permitidas = [
        '.html', '.css', '.php', '.js', '.py', '.json', '.sql', '.md', '.txt', '.ino', '.h'
    ]
    if rapido:
        report_generator.generar_archivo_salida_rapido(
            ruta, extensiones_permitidas
        )
    else:
        report_generator.generar_archivo_salida(
            ruta, modo_prompt, extensiones_permitidas, project_path, incluir_todo
        )
    eventos.append({'type': 'log', 'level': 'info', 'message': f"[BATCH] Análisis finalizado para: {ruta}"})
    for evento in eventos:
        if evento['type'] == 'log' and logger_port:
            getattr(logger_port, evento['level'])(evento['message'])
    return True
