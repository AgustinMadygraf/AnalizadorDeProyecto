"""
API de alto nivel para uso batch/no interactivo del AnalizadorDeProyecto.
Permite invocar análisis y generación de reportes desde CLI o scripts.
"""
from domain.report_generator import ReportGenerator
from interfaces.file_manager_port import FileManagerPort
from interfaces.file_ops_port import FileOpsPort
from interfaces.content_manager_port import ContentManagerPort
from interfaces.clipboard_port import ClipboardPort
from interfaces.logger_port import LoggerPort
from interfaces.event_handler_port import IEventHandlerPort

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
    rapido: bool = False
):
    eventos = []
    eventos.append({'type': 'log', 'level': 'info', 'message': f"[BATCH] Iniciando análisis en: {ruta}"})
    report_generator = ReportGenerator(
        project_path,
        file_manager_port=file_manager_port,
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
