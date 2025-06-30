from colorama import Fore, Style
import time
import threading
import os
from src.presentation.i18n import LANG  # pylint: disable=import-error
import argparse
import logging

logger = logging.getLogger(__name__)

# Detectar si se deben desactivar colores
NO_COLOR = os.environ.get('ANSI_COLORS_DISABLED') == '1'

def _clr(text, color):
    return text if NO_COLOR else f"{color}{text}{Style.RESET_ALL}"


def esperar_usuario(input_func=input):
    respuesta = input_func(_clr(LANG.get('press_enter', '\nPresiona Enter para reiniciar o escribe \'salir\' para terminar...'), Fore.GREEN))
    if respuesta.strip().lower() in ("salir", "exit"):
        logger.info(_clr(LANG.get('bye', '[INFO] Saliendo del AnalizadorDeProyecto. ¡Hasta luego!'), Fore.YELLOW))
        exit(0)

def mostrar_error_ruta():
    logger.error(_clr(LANG.get('error_invalid_option', '[ERROR] La ruta proporcionada no es válida o no se puede acceder a ella.'), Fore.RED))
    logger.info(LANG.get('suggestion', 'Sugerencia: Verifique que la ruta exista, tenga permisos de lectura y sea un directorio válido.'))

def mostrar_info_todo(inc_exc):
    logger.info(_clr(LANG.get('info_processing', '[INFO] Se ha seleccionado la opción de {inc_exc} \"todo.txt\" para análisis.').format(inc_exc=inc_exc), Fore.CYAN))

def limpieza_pantalla():
    logger.info("\033[H\033[J")

def parse_args():
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
    return parser.parse_args()

if __name__ == "__main__":
    from src.application.orchestrator import main_orchestrator
    main_orchestrator()
