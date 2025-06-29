# tests/test_content_manager.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from helper_content_manager import contenido_archivo, filtrar_archivos_por_extension
from unittest.mock import mock_open, patch, MagicMock

def test_contenido_archivo():
    archivos = ['archivo1.txt', 'archivo2.txt']
    contenido_mock = 'contenido de prueba'
    
    m = mock_open(read_data=contenido_mock)
    with patch('builtins.open', m):
        resultado = contenido_archivo(archivos)
        
    assert '--- Contenido de archivo1.txt ---' in resultado
    assert contenido_mock in resultado

def test_contenido_archivo_error():
    archivos = ['archivo1.txt']
    
    m = mock_open()
    m.side_effect = IOError("Error al abrir archivo")
    
    with patch('builtins.open', m):
        resultado = contenido_archivo(archivos)
        
    assert 'Error al leer el archivo archivo1.txt: Error al abrir archivo' in resultado

def test_filtrar_archivos_por_extension():
    archivos = ['archivo1.py', 'archivo2.txt', 'archivo3.md']
    extensiones = ['.py', '.md']
    
    resultado = filtrar_archivos_por_extension(archivos, extensiones)
    
    assert 'archivo1.py' in resultado
    assert 'archivo3.md' in resultado
    assert 'archivo2.txt' not in resultado

