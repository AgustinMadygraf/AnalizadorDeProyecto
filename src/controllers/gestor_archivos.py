# src/controllers/gestor_archivos.py
from src.models.archivo import Archivo

class GestorArchivos:
    def __init__(self, ruta):
        self.ruta = ruta

    def obtener_archivos(self):
        archivos = []
        for raiz, _, archivos_en_ruta in os.walk(self.ruta):
            for nombre_archivo in archivos_en_ruta:
                archivos.append(Archivo(os.path.join(raiz, nombre_archivo)))
        return archivos
