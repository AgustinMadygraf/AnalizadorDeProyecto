import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gestion_archivos import filtrar_archivos_por_extension


class TestFiltrarArchivosPorExtension(unittest.TestCase):

    def test_filtrado_correcto(self):
        archivos = ["foto.jpg", "documento.txt", "script.py", "tabla.xlsx"]
        extensiones = [".txt", ".py"]
        esperado = ["documento.txt", "script.py"]
        resultado = filtrar_archivos_por_extension(archivos, extensiones)
        self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()
