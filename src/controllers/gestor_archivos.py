# src/controllers/gestor_archivos.py

import os
from src.models.archivo import Archivo

class GestorArchivos:
    def __init__(self, ruta):
        self.ruta = ruta

    def obtener_archivos(self):
        archivos = []
        for raiz, _, archivos_en_ruta in os.walk(self.ruta):
            for nombre_archivo in archivos_en_ruta:
                archivos.append(Archivo(os.path.normpath(os.path.join(raiz, nombre_archivo))))
        return archivos

    def buscar_archivo(self, nombre):
        for archivo in self.obtener_archivos():
            if archivo.nombre == nombre:
                return archivo
        return None

    def buscar_archivos_por_extension(self, extension):
        return [archivo for archivo in self.obtener_archivos() if archivo.ruta.endswith(extension)]

    def mover_archivo(self, archivo, nueva_ruta):
        os.rename(archivo.ruta, nueva_ruta)
        archivo.ruta = nueva_ruta
