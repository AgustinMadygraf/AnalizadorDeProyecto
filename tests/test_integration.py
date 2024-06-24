# AnalizadorDeProeyctos/src/test_integration.py
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.app import run_app

# Prueba de integración para la función principal run_app
@patch("builtins.input", side_effect=["S", "N", "test_path", "config\\prompt_1.md", ""])
@patch("src.app.obtener_ruta_default", return_value="test_path")
@patch("src.app.validar_ruta", return_value=True)
@patch("src.app.procesar_archivos", return_value="test_path\\docs\\00-Prompt-for-ProjectAnalysis.md")
def test_run_app(mock_procesar_archivos, mock_validar_ruta, mock_obtener_ruta_default, mock_input):
    with patch("src.app.limpieza_pantalla"), \
         patch("src.app.bienvenida"), \
         patch("src.app.obtener_version_python", return_value='3.9.1'):
        run_app(input_func=input)
        mock_procesar_archivos.assert_called_once_with("test_path", "config\\prompt_1.md", "test_path")
