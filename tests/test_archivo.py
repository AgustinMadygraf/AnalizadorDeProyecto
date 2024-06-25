# tests/test_archivo.py
import unittest
from src.models.archivo import Archivo

class TestArchivo(unittest.TestCase):
    def test_leer_contenido(self):
        archivo = Archivo('ruta/al/archivo.txt')
        contenido = archivo.leer_contenido()
        self.assertIsNotNone(contenido)

    def test_obtener_tamano(self):
        archivo = Archivo('ruta/al/archivo.txt')
        tamano = archivo.obtener_tamano()
        self.assertGreater(tamano, 0)

if __name__ == "__main__":
    unittest.main()
