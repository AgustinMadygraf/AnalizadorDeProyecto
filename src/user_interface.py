# AnalizadorDeProyectos\src\user_interface.py
from colorama import Fore, Style
from src.models.user_interface import UserInterface

ui = UserInterface()

def menu_0():
    return ui.menu_0()

def menu_1():
    opciones = {
        '0': 'config\\prompt_0.md',
        '1': 'config\\prompt_1.md',
        '2': 'config\\prompt_2.md',
        '3': 'config\\prompt_3.md',
        '4': 'config\\prompt_4.md',
        '5': 'config\\prompt_5.md' 
    }

    ui.logger.info("Por favor, seleccione una opción de configuración:")
    ui.logger.info("0 - vacío")
    ui.logger.info("1 - Análisis y Mejora Estructurada del Código para Incrementar Rendimiento y Mantenibilidad")
    ui.logger.info("2 - SOLID: Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas")
    ui.logger.info("3 - POO: Comprensión y Mejora de Proyectos de Software para Dominar la Programación Orientada a Objetos")
    ui.logger.info("4 - TODO.txt: Mejora de la Organización y Productividad en Proyectos de Software con todo.txt")
    ui.logger.info("5 - Testing de aplicaciones: Análisis y Mejora de la Calidad de Software con Pruebas Automatizadas")
    print("")
    eleccion = input(f"{Fore.GREEN}Ingrese el número de la opción deseada: {Style.RESET_ALL}") or '0'
    while eleccion not in opciones:
        ui.logger.info("Opción no válida. Por defecto se seleccionará la opción 0.")
        eleccion = 0
    archivo_seleccionado = opciones[eleccion]
    ui.logger.info(f"Ha seleccionado la opción {eleccion}")
    print("")
    return archivo_seleccionado
