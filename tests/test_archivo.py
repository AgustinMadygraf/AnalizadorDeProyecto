# tests/test_archivo.py
import unittest
from unittest.mock import mock_open, patch
from src.models.archivo import Archivo

class TestArchivo(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='contenido del archivo')
    def test_leer_contenido(self, mock_file):
        archivo = Archivo('ruta/al/archivo.txt')
        contenido = archivo.leer_contenido()
        self.assertEqual(contenido, 'contenido del archivo')
    
    @patch('os.path.getsize', return_value=1024)
    def test_obtener_tamano(self, mock_getsize):
        archivo = Archivo('ruta/al/archivo.txt')
        tamano = archivo.obtener_tamano()
        self.assertEqual(tamano, 1024)

if __name__ == "__main__":
    unittest.main()
