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

    @patch('os.walk')
    @patch('src.models.archivo.Archivo', autospec=True)
    def test_buscar_archivos_por_extension(self, MockArchivo, mock_walk):
        mock_walk.return_value = [
            ('ruta/al/proyecto', ('subdir',), ('archivo1.txt', 'archivo2.py')),
        ]
        MockArchivo.side_effect = lambda ruta: Archivo(ruta)

        archivos = self.gestor.buscar_archivos_por_extension('.py')
        self.assertEqual(len(archivos), 1)
        self.assertEqual(archivos[0].ruta, os.path.normpath('ruta/al/proyecto/archivo2.py'))

    @patch('os.rename')
    def test_mover_archivo(self, mock_rename):
        archivo = Archivo('ruta/al/proyecto/archivo1.txt')
        self.gestor.mover_archivo(archivo, 'ruta/nueva/archivo1.txt')
        mock_rename.assert_called_once_with('ruta/al/proyecto/archivo1.txt', 'ruta/nueva/archivo1.txt')
        self.assertEqual(archivo.ruta, 'ruta/nueva/archivo1.txt')

if __name__ == "__main__":
    unittest.main()
