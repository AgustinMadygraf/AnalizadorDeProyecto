# tests/test_app.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from application.main_app import obtener_extensiones_permitidas, listar_archivos_en_ruta, generar_reporte
from unittest.mock import MagicMock

def test_obtener_extensiones_permitidas():
    extensiones = obtener_extensiones_permitidas()
    assert extensiones == ['.html', '.css', '.php', '.js', '.py', '.json', '.sql', '.md', '.txt', '.ino', '.h']

def test_generar_reporte(mocker):
    mock_report_generator = MagicMock()
    mock_generar_archivo_salida = mocker.patch.object(mock_report_generator, 'generar_archivo_salida')
    # Ajuste: la función generar_reporte acepta 6 argumentos
    generar_reporte('/ruta', 'modo_prompt', '/project_path', mock_report_generator, ['.py'], True)
    mock_generar_archivo_salida.assert_called_once_with('/ruta', 'modo_prompt', ['.py'], '/project_path', True)
