# src/models/user_interface.py

from colorama import Fore, Style
from src.logs.config_logger import LoggerConfigurator

class UserInterface:
    def __init__(self):
        self.logger = LoggerConfigurator().get_logger()

    def solicitar_opcion(self, mensaje, opciones):
        self.logger.debug("Inicio de la selección del modo de operación.")
        while True:
            self.logger.info(mensaje)
            try:
                opcion = int(input())
                if opcion in opciones:
                    return opciones[opcion]
                else:
                    self.logger.warning("Opción no válida. Intente de nuevo.")
            except ValueError:
                self.logger.warning("Entrada no válida. Debes ingresar un número.")

    def menu_0(self):
        self.logger.info("Por favor, introduzca la ruta de la carpeta: ")
        return input().strip()

    def menu_1(self):
        opciones = {
            '0': 'config\\prompt_0.md',
            '1': 'config\\prompt_1.md',
            '2': 'config\\prompt_2.md',
            '3': 'config\\prompt_3.md',
            '4': 'config\\prompt_4.md',
            '5': 'config\\prompt_5.md' 
        }

        self.logger.info("Por favor, seleccione una opción de configuración:")
        self.logger.info("0 - vacío")
        self.logger.info("1 - Análisis y Mejora Estructurada del Código para Incrementar Rendimiento y Mantenibilidad")
        self.logger.info("2 - SOLID: Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas")
        self.logger.info("3 - POO: Comprensión y Mejora de Proyectos de Software para Dominar la Programación Orientada a Objetos")
        self.logger.info("4 - TODO.txt: Mejora de la Organización y Productividad en Proyectos de Software con todo.txt")
        self.logger.info("5 - Testing de aplicaciones: Análisis y Mejora de la Calidad de Software con Pruebas Automatizadas")
        print("")
        eleccion = input(f"{Fore.GREEN}Ingrese el número de la opción deseada: {Style.RESET_ALL}") or '0'
        while eleccion not in opciones:
            self.logger.info("Opción no válida. Por defecto se seleccionará la opción 0.")
            eleccion = 0
        archivo_seleccionado = opciones[eleccion]
        self.logger.info(f"Ha seleccionado la opción {eleccion}")
        print("")
        return archivo_seleccionado
