from colorama import Fore, Style
import time
import threading

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

def esperar_usuario(input_func=input):
    respuesta = input_func(f"{Fore.GREEN}\nPresiona Enter para reiniciar o escribe 'salir' para terminar...{Style.RESET_ALL}")
    if respuesta.strip().lower() in ("salir", "exit"):
        print(f"{Fore.YELLOW}Saliendo del AnalizadorDeProyecto. ¡Hasta luego!{Style.RESET_ALL}")
        exit(0)
