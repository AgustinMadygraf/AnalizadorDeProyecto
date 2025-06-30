"""
Orquestador principal de dependencias y modos de ejecución para AnalizadorDeProyecto.
Extraído de run.py para cumplir Clean Architecture.
"""
import sys
import os
import argparse
from colorama import init
from src.application.batch_api import analizar_y_generar_reporte
from src.application.main_app import run_app
from src.interfaces.file_manager_port import FileManagerPort
from src.interfaces.file_ops_port import FileOpsPort
from src.interfaces.content_manager_port import ContentManagerPort
from src.interfaces.clipboard_port import ClipboardPort
from src.interfaces.logger_port import LoggerPort
from src.interfaces.logger_event_port import LoggerEventPort
from src.interfaces.event_handler_port import IEventHandlerPort
from src.interfaces.file_handler_factory_port import FileHandlerFactoryPort
from src.interfaces.vulture_port import VulturePort
import logging


def main_orchestrator(
    argv=None,
    handler_factory: FileHandlerFactoryPort = None,
    file_manager_port: FileManagerPort = None,
    logger_port: LoggerPort = None,
    logger_event_port: LoggerEventPort = None,
    file_ops_port: FileOpsPort = None,
    content_manager_port: ContentManagerPort = None,
    clipboard_port: ClipboardPort = None,
    event_handler_port: IEventHandlerPort = None,
    vulture_port: VulturePort = None
):
    parser = argparse.ArgumentParser(
        description='AnalizadorDeProyecto: analiza y documenta proyectos de software.',
        epilog='''\nEjemplos de uso:\n  python run.py --input ./mi_proyecto --output reporte.txt --modo completo --incluir-todo --no-interactive\n  python run.py  # modo interactivo clásico\n\nFlags:\n  --input, -i           Ruta del directorio o archivo a analizar (obligatorio en modo batch)\n  --output, -o          Ruta del archivo de salida (opcional)\n  --modo, -m            Modo de análisis (resumen o completo)\n  --incluir-todo        Incluir el archivo todo.txt en el análisis\n  --no-interactive      Ejecutar en modo batch/no interactivo\n  --help, -h            Mostrar esta ayuda y salir\n''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', '-i', help='Ruta del directorio o archivo a analizar')
    parser.add_argument('--output', '-o', help='Ruta del archivo de salida (opcional)')
    parser.add_argument('--modo', '-m', help='Modo de análisis (ej: resumen, completo)', default='resumen')
    parser.add_argument('--incluir-todo', action='store_true', help="Incluir 'todo.txt' en el análisis")
    parser.add_argument('--no-interactive', action='store_true', help='Ejecutar en modo batch/no interactivo')
    parser.add_argument('--no-color', action='store_true', help='Desactivar colores ANSI en la salida')
    parser.add_argument('--lang', help='Idioma de la interfaz (es|en). También configurable con ANALIZADOR_LANG.', default=None)
    args = parser.parse_args(argv)

    logger = logger_port if logger_port else logging.getLogger(__name__)

    disable_colors = args.no_color or not sys.stdout.isatty()
    if disable_colors:
        os.environ['ANSI_COLORS_DISABLED'] = '1'
        try:
            init(strip=True)
        except ImportError:
            pass

    repo_path = os.path.dirname(os.path.abspath(__file__))
    try:
        lang = args.lang or os.environ.get('ANALIZADOR_LANG', 'es')
        MESSAGES = {
            'es': {
                'batch_done': '[INFO] Análisis batch finalizado.',
                'input_not_found': '[ERROR] Ruta de entrada no encontrada:',
                'input_suggestion': 'Sugerencia: Verifique que la ruta especificada con --input exista y sea accesible.',
                'batch_fail': '[ERROR] Fallo en el análisis:',
                'batch_fail_suggestion': 'Sugerencia: Revise los permisos de archivos y el formato de entrada.',
                'interrupted': '\nEjecución interrumpida por el usuario. Saliendo del programa...',
                'unexpected': '[ERROR] Error inesperado en modo interactivo:',
                'unexpected_suggestion': 'Sugerencia: Revise la configuración y reporte el error si persiste.'
            },
            'en': {
                'batch_done': '[INFO] Batch analysis completed.',
                'input_not_found': '[ERROR] Input path not found:',
                'input_suggestion': 'Tip: Check that the path specified with --input exists and is accessible.',
                'batch_fail': '[ERROR] Analysis failed:',
                'batch_fail_suggestion': 'Tip: Check file permissions and input format.',
                'interrupted': '\nExecution interrupted by user. Exiting...',
                'unexpected': '[ERROR] Unexpected error in interactive mode:',
                'unexpected_suggestion': 'Tip: Check configuration or report the error if it persists.'
            }
        }
        TXT = MESSAGES['en'] if lang == 'en' else MESSAGES['es']

        import json
        config_defaults = {}
        config_path = os.path.join(os.path.dirname(__file__), '.analizadorrc')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_defaults = json.load(f)
            except json.JSONDecodeError as e:
                logger.warning("No se pudo leer .analizadorrc (JSON inválido): %s", e)
            except OSError as e:
                logger.warning("No se pudo acceder a .analizadorrc: %s", e)
        for key, value in config_defaults.items():
            if getattr(args, key, None) in (None, False):
                setattr(args, key, value)

        if args.no_interactive:
            if not args.input:
                logger.error("%s <stdin>", TXT['input_not_found'])
                logger.info(TXT['input_suggestion'])
                sys.exit(1)

        if args.no_interactive and args.input:
            # Validar existencia de la ruta antes de analizar
            if args.input != '-' and not os.path.exists(args.input):
                logger.error("%s %s", TXT['input_not_found'], args.input)
                logger.info(TXT['input_suggestion'])
                sys.exit(1)
            if args.input == '-':
                import tempfile
                temp_input = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', suffix='.tmp')
                for line in sys.stdin:
                    temp_input.write(line)
                temp_input.flush()
                temp_input.close()
                input_path = temp_input.name
            else:
                input_path = args.input
            try:
                analizar_y_generar_reporte(
                    ruta=input_path,
                    modo_prompt=args.modo,
                    project_path=repo_path,
                    incluir_todo=args.incluir_todo,
                    file_manager_port=file_manager_port,
                    file_ops_port=file_ops_port,
                    content_manager_port=content_manager_port,
                    clipboard_port=clipboard_port,
                    logger_port=logger_port,
                    event_handler_port=event_handler_port,
                    rapido=(args.modo.strip().lower() in ["rapido", "resumen", "estructura"]),
                    handler_factory=handler_factory
                )
                logger.info(TXT['batch_done'])
                sys.exit(0)
            except FileNotFoundError as e:
                logger.error("%s %s", TXT['input_not_found'], e)
                logger.info(TXT['input_suggestion'])
                sys.exit(1)
            except (PermissionError, IsADirectoryError, OSError, ValueError) as e:
                logger.error("%s %s", TXT['batch_fail'], e)
                logger.info(TXT['batch_fail_suggestion'])
                sys.exit(2)
            except RuntimeError as e:
                import traceback
                logger.error("%s %s", TXT['batch_fail'], e)
                logger.error(traceback.format_exc())
                logger.info(TXT['batch_fail_suggestion'])
                sys.exit(2)
            except Exception as e:
                raise
        else:
            run_app(
                file_manager_port=file_manager_port,
                file_ops_port=file_ops_port,
                content_manager_port=content_manager_port,
                clipboard_port=clipboard_port,
                logger_event_port=logger_event_port,
                event_handler_port=event_handler_port,
                handler_factory=handler_factory
            )
            sys.exit(0)
    except KeyboardInterrupt:
        logger.info(TXT['interrupted'])
        sys.exit(130)

    # Ejemplo de uso de VulturePort (ajustar según integración real)
    # nombres = vulture_port.extract_names('src')
    # refs = vulture_port.find_references('nombre_funcion', ['src/domain', 'src/application'])
    # plan = vulture_port.generate_removal_plan('infrastructure/vulture/vulture_report.txt')
