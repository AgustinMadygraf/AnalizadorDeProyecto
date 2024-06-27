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
