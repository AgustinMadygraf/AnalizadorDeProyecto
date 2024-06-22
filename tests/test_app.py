#AnalizadorDeProyectos/tests/test_app.py
import sys
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock


from ..src.app import (
    obtener_ruta_analisis,
    seleccionar_modo_operacion,
    inicializar,
    bienvenida,
    guardar_nueva_ruta_default,
    obtener_ruta_default,
    obtener_ruta_script,
    validar_ruta,
    procesar_archivos,
    crear_archivo_path_json
)

@patch('builtins.input', return_value='S')
@patch('app.obtener_ruta_default', return_value='test_path')
def test_obtener_ruta_analisis(mock_obtener_ruta_default, mock_input):
    ruta = obtener_ruta_analisis('test_project_path', input_func=mock_input)
    assert ruta == 'test_path'

def test_seleccionar_modo_operacion():
    with patch('builtins.input', return_value='1'):
        modo_prompt = seleccionar_modo_operacion(input_func=input)
        assert modo_prompt == 'config\\prompt_1.md'

@patch('builtins.input', return_value='')
def test_inicializar(mock_input):
    with patch('app.limpieza_pantalla'), \
         patch('app.bienvenida'), \
         patch('app.obtener_version_python', return_value='3.9.1'):
        project_path = inicializar()
        assert os.path.isdir(project_path)

@patch('builtins.input', return_value='test_path')
def test_guardar_nueva_ruta_default(mock_input):
    with patch('builtins.open', mock_open(read_data='{"rutas": []}')) as mock_file:
        guardar_nueva_ruta_default('test_path')
        mock_file.assert_called_with('config/path.json', 'w', encoding='utf-8')

@patch('builtins.input', return_value='1')
def test_obtener_ruta_default(mock_input):
    with patch('builtins.open', mock_open(read_data='{"rutas": [{"ruta": "test_path", "ultimo_acceso": "2024-06-22T00:00:00"}]}')):
        ruta = obtener_ruta_default(input_func=mock_input)
        assert ruta == 'test_path'

def test_obtener_ruta_script():
    ruta_script = obtener_ruta_script()
    assert os.path.isdir(ruta_script)

def test_validar_ruta():
    assert validar_ruta('.') == True
    assert validar_ruta('non_existent_path') == False

def test_procesar_archivos():
    with patch('app.listar_archivos', return_value=[]), \
         patch('app.generar_archivo_salida', return_value='test_path\\docs\\00-Prompt-for-ProjectAnalysis.md'):
        resultado = procesar_archivos('test_path', 'config\\prompt_1.md', 'test_project_path')
        assert resultado == 'test_path\\docs\\00-Prompt-for-ProjectAnalysis.md'

def test_crear_archivo_path_json():
    with patch('builtins.open', mock_open()) as mock_file, \
         patch('os.makedirs') as mock_makedirs:
        if not os.path.exists('config'):
            mock_makedirs.return_value = None
        crear_archivo_path_json()
        mock_makedirs.assert_called_with('config')
        mock_file.assert_called_with('config/path.json', 'w', encoding='utf-8')
