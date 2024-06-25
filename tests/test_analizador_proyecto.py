# tests/test_analizador_proyecto.py

import unittest
from unittest.mock import patch, mock_open
from src.controllers.analizador_proyecto import AnalizadorDeProyecto
from src.models.archivo import Archivo

class TestAnalizadorDeProyecto(unittest.TestCase):
    @patch('src.controllers.gestor_archivos.GestorArchivos.obtener_archivos')
    def test_analizar(self, mock_obtener_archivos):
        mock_obtener_archivos.return_value = [
            Archivo('ruta/al/proyecto/archivo1.txt'),
            Archivo('ruta/al/proyecto/archivo2.txt')
        ]
        analizador = AnalizadorDeProyecto('ruta/al/proyecto')
        analizador.analizar()
        self.assertEqual(len(analizador.proyecto.archivos), 2)

    @patch('os.path.getsize', side_effect=lambda x: 1024)
    @patch('builtins.open', new_callable=mock_open, read_data="print('Hello World')\n# This is a comment\n\nprint('Goodbye World')")
    def test_generar_reporte(self, mock_open, mock_getsize):
        analizador = AnalizadorDeProyecto('ruta/al/proyecto')
        archivo1 = Archivo('ruta/al/proyecto/archivo1.txt')
        archivo2 = Archivo('ruta/al/proyecto/archivo2.txt')
        analizador.proyecto.agregar_archivo(archivo1)
        analizador.proyecto.agregar_archivo(archivo2)
        reporte = analizador.generar_reporte()
        self.assertIn("Total de Archivos: 2", reporte)
        self.assertIn("Archivo: ruta/al/proyecto/archivo1.txt - Tamaño: 1024 bytes - Líneas de Código: 2", reporte)
        self.assertIn("Archivo: ruta/al/proyecto/archivo2.txt - Tamaño: 1024 bytes - Líneas de Código: 2", reporte)

if __name__ == "__main__":
    unittest.main()
