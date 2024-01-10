import unittest
import os
import sys

# Añadir la carpeta superior al PATH de Python
ruta_directorio_superior = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_directorio_superior)

from gestion_archivos import listar_archivos, escribir_contenido_archivo

class TestGestionArchivos(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        pass

    def test_listar_archivos(self):
        # Aquí tus pruebas para listar_archivos
        pass

    def test_escribir_contenido_archivo(self):
        # Aquí tus pruebas para escribir_contenido_archivo
        pass

    def tearDown(self):
        # Limpieza después de cada prueba
        pass

if __name__ == '__main__':
    unittest.main()
