# src/models/proyecto.py
class Proyecto:
    def __init__(self, ruta):
        self.ruta = ruta
        self.archivos = []

    def agregar_archivo(self, archivo):
        self.archivos.append(archivo)

    def listar_archivos(self):
        return [archivo.ruta for archivo in self.archivos]
