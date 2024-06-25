#AnalizadorDeProyectos/tests/test_path_manager.py
import os
import pytest
import json
from datetime import datetime
from unittest.mock import patch, mock_open

from src.path_manager import (
    obtener_ruta_analisis,
    crear_archivo_path_json,
    guardar_nueva_ruta_default,
    obtener_ruta_default,
    obtener_ruta_script,
    validar_ruta
)

@patch('builtins.input', return_value='S')
@patch('src.path_manager.obtener_ruta_default', return_value='test_path')
def test_obtener_ruta_analisis(mock_obtener_ruta_default, mock_input):
    ruta = obtener_ruta_analisis('test_project_path', input_func=mock_input)
    assert ruta == 'test_path'

@patch("builtins.open", new_callable=mock_open)
def test_crear_archivo_path_json(mock_file):
    with patch('os.path.exists', return_value=False), patch('os.makedirs') as mock_makedirs:
        crear_archivo_path_json()
        mock_makedirs.assert_called_once_with('config')
        mock_file.assert_called_once_with(os.path.join('config', 'path.json').replace('/', '\\'), 'w', encoding='utf-8')

@patch("builtins.open", new_callable=mock_open, read_data='{"rutas": [{"ruta": "test_path", "ultimo_acceso": "2024-06-22T00:00:00"}]}')
def test_obtener_ruta_default(mock_file):
    with patch('os.path.exists', return_value=True):
        ruta = obtener_ruta_default(input_func=lambda _: '1')
        assert ruta == 'test_path'

def test_obtener_ruta_script():
    ruta_script = obtener_ruta_script()
    assert os.path.isdir(ruta_script)

def test_validar_ruta():
    assert validar_ruta('.') == True
    assert validar_ruta('non_existent_path') == False
