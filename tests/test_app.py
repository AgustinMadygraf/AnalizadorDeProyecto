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
