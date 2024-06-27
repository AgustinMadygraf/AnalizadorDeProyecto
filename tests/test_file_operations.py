# tests/test_file_operations.py
import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from src.file_operations import listar_archivos

# Prueba para la función listar_archivos
@patch('os.walk')
@patch('os.path.getsize', return_value=1024)
@patch('src.file_operations.contar_lineas_codigo', return_value=10)
def test_listar_archivos(mock_contar_lineas, mock_getsize, mock_walk):
    mock_walk.return_value = [
        ('/ruta', ('subdir',), ('archivo1.py', 'archivo2.txt')),
        ('/ruta/subdir', (), ('archivo3.py',)),
    ]
    
    archivos, estructura = listar_archivos('/ruta', {'.py', '.txt'})
    
    assert len(archivos) == 3
    assert 'archivo1.py' in archivos[0]
    assert 'archivo2.txt' in archivos[1]
    assert 'archivo3.py' in archivos[2]
    assert len(estructura) == 5  # Ajuste para reflejar la estructura real

@patch('os.walk')
@patch('os.path.getsize', return_value=1024)
@patch('src.file_operations.contar_lineas_codigo', return_value=10)
def test_listar_archivos_sin_extension(mock_contar_lineas, mock_getsize, mock_walk):
    mock_walk.return_value = [
        ('/ruta', ('subdir',), ('archivo1.py', 'archivo2.txt')),
        ('/ruta/subdir', (), ('archivo3.py',)),
    ]
    
    archivos, estructura = listar_archivos('/ruta', None)
    
    assert len(archivos) == 3
