from colorama import Fore, Style
import time
import threading
import os

# Detectar si se deben desactivar colores
NO_COLOR = os.environ.get('ANSI_COLORS_DISABLED') == '1'

def _clr(text, color):
    return text if NO_COLOR else f"{color}{text}{Style.RESET_ALL}"

def bienvenida(input_func=input):
    mensaje = """Bienvenido al AnalizadorDeProyecto 🌟\nEste software es una herramienta avanzada diseñada para ayudarte a analizar, documentar y mejorar la estructura de tus proyectos de software...\n    ¡Esperamos que disfrutes utilizando esta herramienta y que te sea de gran ayuda en tus proyectos de software!"""
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
    respuesta = input_func(_clr("\nPresiona Enter para reiniciar o escribe 'salir' para terminar...", Fore.GREEN))
    if respuesta.strip().lower() in ("salir", "exit"):
        print(_clr("[INFO] Saliendo del AnalizadorDeProyecto. ¡Hasta luego!", Fore.YELLOW))
        exit(0)

def mostrar_error_ruta():
    print(_clr("[ERROR] La ruta proporcionada no es válida o no se puede acceder a ella.", Fore.RED))
    print("Sugerencia: Verifique que la ruta exista, tenga permisos de lectura y sea un directorio válido.")

def mostrar_info_todo(inc_exc):
    print(_clr(f"[INFO] Se ha seleccionado la opción de {inc_exc} 'todo.txt' para análisis.", Fore.CYAN))

def limpieza_pantalla():
    print("\033[H\033[J", end="")
