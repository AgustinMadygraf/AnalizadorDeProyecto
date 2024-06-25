import os
import pytest
from unittest.mock import patch, mock_open

from src.app import (
    obtener_ruta_analisis,
    procesar_archivos
)

from src.app import (
    seleccionar_modo_operacion,
    inicializar,
    bienvenida,
    run_app
)

@patch('builtins.input', return_value='S')
@patch('src.path_manager.obtener_ruta_default', return_value='test_path')
@patch('src.path_manager.validar_ruta', return_value=True)
@patch('src.app.procesar_archivos')
@patch('src.app.limpieza_pantalla')

def test_seleccionar_modo_operacion():
    with patch('builtins.input', return_value='1'):
        modo_prompt = seleccionar_modo_operacion(input_func=input)
        assert modo_prompt == 'config\\prompt_1.md'

@patch('builtins.input', return_value='')
def test_inicializar(mock_input):
    with patch('src.app.limpieza_pantalla'), \
         patch('src.app.bienvenida'), \
         patch('src.utilities.obtener_version_python', return_value='3.9.1'):
        project_path = inicializar()
        assert os.path.isdir(project_path)

@patch('builtins.input', return_value='Presiona Enter para continuar...')
def test_bienvenida(mock_input):
    with patch('src.app.time.sleep', return_value=None):
        bienvenida(input_func=mock_input)
