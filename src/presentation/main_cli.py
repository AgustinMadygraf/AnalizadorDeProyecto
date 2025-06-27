from colorama import Fore, Style
import time
import threading
import os
from common.i18n import LANG

# Detectar si se deben desactivar colores
NO_COLOR = os.environ.get('ANSI_COLORS_DISABLED') == '1'

def _clr(text, color):
    return text if NO_COLOR else f"{color}{text}{Style.RESET_ALL}"

def bienvenida(input_func=input):
    mensaje = LANG.get("menu_main_title", "Bienvenido al AnalizadorDeProyecto 🌟") + "\n" + \
        "Este software es una herramienta avanzada diseñada para ayudarte a analizar, documentar y mejorar la estructura de tus proyectos de software...\n    ¡Esperamos que disfrutes utilizando esta herramienta y que te sea de gran ayuda en tus proyectos de software!"
    mensaje = f"{mensaje}\n\n\nPresiona Enter para continuar...\n"
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

def esperar_usuario(input_func=input):
    respuesta = input_func(_clr(LANG.get('press_enter', '\nPresiona Enter para reiniciar o escribe \'salir\' para terminar...'), Fore.GREEN))
    if respuesta.strip().lower() in ("salir", "exit"):
        print(_clr(LANG.get('bye', '[INFO] Saliendo del AnalizadorDeProyecto. ¡Hasta luego!'), Fore.YELLOW))
        exit(0)

def mostrar_error_ruta():
    print(_clr(LANG.get('error_invalid_option', '[ERROR] La ruta proporcionada no es válida o no se puede acceder a ella.'), Fore.RED))
    print(LANG.get('suggestion', 'Sugerencia: Verifique que la ruta exista, tenga permisos de lectura y sea un directorio válido.'))

def mostrar_info_todo(inc_exc):
    print(_clr(LANG.get('info_processing', '[INFO] Se ha seleccionado la opción de {inc_exc} \"todo.txt\" para análisis.').format(inc_exc=inc_exc), Fore.CYAN))

def limpieza_pantalla():
    print("\033[H\033[J", end="")
