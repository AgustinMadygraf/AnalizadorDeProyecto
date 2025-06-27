"""
API de alto nivel para uso batch/no interactivo del AnalizadorDeProyecto.
Permite invocar análisis y generación de reportes desde CLI o scripts.
"""
from domain.report_generator import ReportGenerator
from interfaces.file_manager_port import FileManagerPort
from interfaces.file_ops_port import FileOpsPort
from interfaces.content_manager_port import ContentManagerPort
from interfaces.clipboard_port import ClipboardPort

def analizar_y_generar_reporte(
    ruta: str,
    modo_prompt: str,
    project_path: str,
    incluir_todo: bool,
    file_manager_port: FileManagerPort,
    file_ops_port: FileOpsPort,
    content_manager_port: ContentManagerPort,
    clipboard_port: ClipboardPort,
    event_handler=None
):
    """
    Ejecuta el análisis y genera el reporte, sin interacción de usuario.
    """
    report_generator = ReportGenerator(
        project_path,
        file_manager_port=file_manager_port,
        file_ops_port=file_ops_port,
        content_manager_port=content_manager_port,
        clipboard_port=clipboard_port,
        event_handler=event_handler
    )
    extensiones_permitidas = [
        '.html', '.css', '.php', '.js', '.py', '.json', '.sql', '.md', '.txt', '.ino', '.h'
    ]
    report_generator.generar_archivo_salida(
        ruta, modo_prompt, extensiones_permitidas, project_path, incluir_todo
    )
    return True
