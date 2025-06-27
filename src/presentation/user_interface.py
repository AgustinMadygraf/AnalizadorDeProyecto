# src/presentation/user_interface.py

from colorama import Fore, Style
from tabulate import tabulate
import json
import os
import datetime
from common.i18n import LANG

class UserInterface:
    def __init__(self, logger_port):
        self.logger = logger_port

    def solicitar_opcion(self, mensaje, opciones):
        self.logger.debug("Inicio de la selección del modo de operación.")
        while True:
            self.logger.info(mensaje)
            try:
                opcion = input(LANG.get('prompt_select_option', 'Seleccione una opción: ')).strip()
                if opcion in opciones:
                    return opciones[opcion]
                else:
                    self.logger.warning(LANG.get('error_invalid_option', 'Opción no válida. Intente de nuevo.'))
            except ValueError:
                self.logger.warning(LANG.get('error_invalid_option', 'Entrada no válida. Debes ingresar un número.'))

    def menu_0(self):
        self.logger.info(LANG.get('prompt_enter_path', 'Por favor, introduzca la ruta de la carpeta: '))
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

        headers = [LANG.get('menu_option', 'Opción'), LANG.get('menu_description', 'Descripción')]
        tabla = [
            ["0", LANG.get('submenu_option_0', 'Vacío')],
            ["1", LANG.get('submenu_option_1', 'Análisis y Mejora Estructurada del Código para Incrementar Rendimiento y Mantenibilidad')],
            ["2", LANG.get('submenu_option_2', 'SOLID: Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas')],
            ["3", LANG.get('submenu_option_3', 'POO: Comprensión y Mejora de Proyectos de Software para Dominar la Programación Orientada a Objetos')],
            ["4", LANG.get('submenu_option_4', 'Software Engineering: Análisis y Mejora de Proyectos de Software con Técnicas de Ingeniería de Software')],
            ["5", LANG.get('submenu_option_5', 'Asesor de Calidad de Software ISO 90003')],
            ["6", LANG.get('submenu_option_6', 'Testing de aplicaciones: Análisis y Mejora de la Calidad de Software con Pruebas Automatizadas')]
        ]
        print(tabulate(tabla, headers, tablefmt="fancy_grid"))
        return input(LANG.get('prompt_select_option', 'Seleccione una opción: ')).strip()
