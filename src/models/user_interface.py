# src/models/user_interface.py

from colorama import Fore, Style
from src.logs.config_logger import LoggerConfigurator
from tabulate import tabulate
import json
import os
import datetime

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

        headers = ["Opción", "Descripción"]
        tabla = [
            ["0", "vacío"],
            ["1", "Análisis y Mejora Estructurada del Código para Incrementar Rendimiento y Mantenibilidad"],
            ["2", "SOLID: Evaluación y Optimización de Código Python según Principios SOLID con Pruebas Automatizadas"],
            ["3", "POO: Comprensión y Mejora de Proyectos de Software para Dominar la Programación Orientada a Objetos"],
            ["4", "TODO.txt: Mejora de la Organización y Productividad en Proyectos de Software con todo.txt"],
            ["5", "Testing de aplicaciones: Análisis y Mejora de la Calidad de Software con Pruebas Automatizadas"]
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
        print("")
        return archivo_seleccionado

    def obtener_ruta_default(self, input_func=input):
        archivo_default = 'config/path.json'
        if not os.path.exists(archivo_default):
            self.logger.info(f"El archivo {archivo_default} no existe. Creando uno nuevo.")
            self.crear_archivo_path_json()
        try:
            with open(archivo_default, 'r', encoding='utf-8') as file:
                data = json.load(file)
                rutas = data.get('rutas', [])
            
            if not rutas:
                nueva_ruta = input_func("No se encontraron rutas guardadas. Por favor, introduzca una nueva ruta: ").strip()
                self.guardar_nueva_ruta_default(nueva_ruta)
                return nueva_ruta

            # Ordenar las rutas por el último acceso desde la más reciente a la más antigua
            rutas.sort(key=lambda x: x['ultimo_acceso'], reverse=True)

            headers = ["#", "Ruta", "Último Acceso"]
            tabla = [[0, "Introducir nueva ruta", ""]]
            for i, ruta_info in enumerate(rutas, start=1):
                ruta = ruta_info['ruta']
                ultimo_acceso = datetime.datetime.strptime(ruta_info['ultimo_acceso'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y %H:%M")
                tabla.append([i, ruta, ultimo_acceso])

            print(tabulate(tabla, headers, tablefmt="grid"))
            print("")

            while True:
                eleccion = input_func(f"{Fore.GREEN}Seleccione una opción: {Style.RESET_ALL}").strip()
                if not eleccion:
                    return rutas[0]['ruta']
                elif eleccion.isdigit() and 1 <= int(eleccion) < len(tabla):
                    return rutas[int(eleccion)-1]['ruta']
                elif eleccion == '0':
                    nueva_ruta = input_func("Introduzca la nueva ruta: ").strip()
                    self.guardar_nueva_ruta_default(nueva_ruta)
                    return nueva_ruta
                else:
                    self.logger.warning("Opción no válida. Por favor, intente de nuevo.")
                    print(f"{Fore.RED}Opción no válida. Por favor, intente de nuevo.{Style.RESET_ALL}")

        except Exception as e:
            self.logger.error(f"Ocurrió un error: {e}")
        except FileNotFoundError:
            nueva_ruta = input_func("Por favor, introduzca una nueva ruta: ").strip()
            self.guardar_nueva_ruta_default(nueva_ruta)
            return nueva_ruta

    def crear_archivo_path_json(self):
        ruta_directorio = 'config'
        archivo_default = os.path.join(ruta_directorio, 'path.json')

        project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ultimo_acceso = datetime.datetime.now().isoformat()

        contenido_inicial = {
            "rutas": [
                {
                    "ruta": project_path,
                    "ultimo_acceso": ultimo_acceso
                }
            ]
        }

        if not os.path.exists(ruta_directorio):
            os.makedirs(ruta_directorio)
            self.logger.info(f"Directorio {ruta_directorio} creado.")

        try:
            with open(archivo_default, 'w', encoding='utf-8') as file:
                json.dump(contenido_inicial, file, indent=4)
            self.logger.info(f"Archivo {archivo_default} creado con éxito. Ruta del proyecto y fecha/hora actuales añadidas.")
        except Exception as e:
            self.logger.error(f"No se pudo crear el archivo {archivo_default}: {e}")

    def guardar_nueva_ruta_default(self, nueva_ruta):
        archivo_default = 'config/path.json'
        try:
            if os.path.exists(archivo_default):
                with open(archivo_default, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            else:
                data = {"rutas": []}
            
            ruta_existente = next((item for item in data["rutas"] if item["ruta"] == nueva_ruta), None)
            if ruta_existente:
                ruta_existente["ultimo_acceso"] = datetime.datetime.now().isoformat()
            else:
                data["rutas"].insert(0, {"ruta": nueva_ruta, "ultimo_acceso": datetime.datetime.now().isoformat()})
            
            with open(archivo_default, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            
            self.logger.info(f"Nueva ruta por defecto guardada: {nueva_ruta}")
        except Exception as e:
            self.logger.error(f"Error al guardar la nueva ruta por defecto: {e}")
