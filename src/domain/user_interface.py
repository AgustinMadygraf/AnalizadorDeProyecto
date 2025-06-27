# src/domain/user_interface.py

from colorama import Fore, Style
from tabulate import tabulate
import json
import os
import datetime

class UserInterface:
    def __init__(self, logger_port):
        self.logger = logger_port

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

        headers = ["Opción", "Descripción"]
        tabla = [
            ["0", "vacío"],
            ["1", "Análisis y Mejora Estructurada del Código para Incrementar Rendimiento y Mantenibilidad"],
            ["2", "SOLID: Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas"],
            ["3", "POO: Comprensión y Mejora de Proyectos de Software para Dominar la Programación Orientada a Objetos"],
            ["4", "Software Engineering: Análisis y Mejora de Proyectos de Software con Técnicas de Ingeniería de Software"],
            ["5", "Asesor de Calidad de Software ISO 90003"],
            ["6", "Testing de aplicaciones: Análisis y Mejora de la Calidad de Software con Pruebas Automatizadas"]
        ]

        self.logger.info("Por favor, seleccione una opción de configuración:")
        print(tabulate(tabla, headers, tablefmt="grid"))
        print("")
        eleccion = input(f"{Fore.GREEN}Ingrese el número de la opción deseada: {Style.RESET_ALL}") or '0'
        while eleccion not in opciones:
            self.logger.info("Opción no válida. Por defecto se seleccionará la opción 0.")
            eleccion = 0
        archivo_seleccionado = opciones[eleccion]
        self.logger.info(f"Ha seleccionado la opción {eleccion}")
        return archivo_seleccionado

# No hay imports de src.domain, pero si los hubiera, deben ser relativos a la raíz de src.
