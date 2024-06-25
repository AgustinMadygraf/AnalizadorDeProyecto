# src/controllers/analizador_proyecto.py

import os
from src.models.archivo import Archivo
from src.models.proyecto import Proyecto
from src.controllers.gestor_archivos import GestorArchivos


class AnalizadorDeProyecto:
    def __init__(self, ruta_proyecto):
        self.proyecto = Proyecto(ruta_proyecto)
        self.gestor_archivos = GestorArchivos(ruta_proyecto)

    def analizar(self):
        archivos = self.gestor_archivos.obtener_archivos()
        for archivo in archivos:
            self.proyecto.agregar_archivo(archivo)

    def generar_reporte(self):
        reporte = f"Análisis del Proyecto en la Ruta: {self.proyecto.ruta}\n"
        reporte += f"Total de Archivos: {len(self.proyecto.archivos)}\n"
        for archivo in self.proyecto.archivos:
            reporte += f"Archivo: {archivo.ruta} - Tamaño: {archivo.obtener_tamano()} bytes\n"
        return reporte
