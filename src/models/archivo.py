# src/models/archivo.py
import os

class Archivo:
    def __init__(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)

    def leer_contenido(self):
        with open(self.ruta, 'r', encoding='utf-8') as archivo:
            return archivo.read()

    def obtener_tamano(self):
        return os.path.getsize(self.ruta)

    def contar_lineas_codigo(self):
        lineas_codigo = 0
        try:
            with open(self.ruta, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea and not linea.startswith("#"):
                        lineas_codigo += 1
        except Exception as e:
            return f"Error leyendo el archivo {self.ruta}: {e}"
        return lineas_codigo
