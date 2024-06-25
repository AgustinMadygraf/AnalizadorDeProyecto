import pytest
import os
from src.app import manejar_ruta_proyecto, esperar_usuario, inicializar
from unittest.mock import patch

def test_manejar_ruta_proyecto_valida(mocker):
    mocker.patch('src.app.seleccionar_ruta', return_value='ruta_valida')
    mocker.patch('src.app.validar_ruta', return_value=True)
    mocker.patch('src.app.seleccionar_modo_operacion', return_value='modo_prompt')
    mocker.patch('src.app.procesar_archivos')
    
    result = manejar_ruta_proyecto('project_path', input)
    assert result is True

def test_manejar_ruta_proyecto_invalida(mocker):
    mocker.patch('src.app.seleccionar_ruta', return_value='ruta_invalida')
    mocker.patch('src.app.validar_ruta', return_value=False)
    
    result = manejar_ruta_proyecto('project_path', input)
    assert result is False
