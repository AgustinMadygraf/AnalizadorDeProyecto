# src/models/archivo.py
class Archivo:
    def __init__(self, ruta):
        self.ruta = ruta

    def leer_contenido(self):
        with open(self.ruta, 'r', encoding='utf-8') as archivo:
            return archivo.read()

    def obtener_tamano(self):
        return os.path.getsize(self.ruta)
