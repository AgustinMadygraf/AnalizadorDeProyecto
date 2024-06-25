# tests/test_gestor_archivos.py
import unittest
from unittest.mock import patch, mock_open
from src.controllers.gestor_archivos import GestorArchivos
from src.models.archivo import Archivo
import os

class TestGestorArchivos(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorArchivos('ruta/al/proyecto')

    @patch('os.walk')
    @patch('src.models.archivo.Archivo', autospec=True)
    def test_obtener_archivos(self, MockArchivo, mock_walk):
        mock_walk.return_value = [
            ('ruta/al/proyecto', ('subdir',), ('archivo1.txt', 'archivo2.txt')),
        ]
        MockArchivo.side_effect = lambda ruta: Archivo(ruta)

        archivos = self.gestor.obtener_archivos()
        self.assertEqual(len(archivos), 2)
        self.assertEqual(archivos[0].ruta, os.path.normpath('ruta/al/proyecto/archivo1.txt'))
        self.assertEqual(archivos[1].ruta, os.path.normpath('ruta/al/proyecto/archivo2.txt'))

    @patch('os.walk')
    @patch('src.models.archivo.Archivo', autospec=True)
    def test_buscar_archivo(self, MockArchivo, mock_walk):
        mock_walk.return_value = [
            ('ruta/al/proyecto', ('subdir',), ('archivo1.txt', 'archivo2.txt')),
        ]
        MockArchivo.side_effect = lambda ruta: Archivo(ruta)

        archivo = self.gestor.buscar_archivo('archivo1.txt')
        self.assertIsNotNone(archivo)
        self.assertEqual(archivo.ruta, os.path.normpath('ruta/al/proyecto/archivo1.txt'))

if __name__ == "__main__":
    unittest.main()
