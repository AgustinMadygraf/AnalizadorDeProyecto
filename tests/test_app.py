# tests/test_app.py
import pytest
from src.app import obtener_extensiones_permitidas, listar_archivos_en_ruta, generar_reporte
from unittest.mock import MagicMock

def test_obtener_extensiones_permitidas():
    extensiones = obtener_extensiones_permitidas()
    assert extensiones == ['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt', '.ino', '.h']

def test_listar_archivos_en_ruta(mocker):
    mock_listar_archivos = mocker.patch('src.file_operations.listar_archivos', return_value=(['archivo1.py'], []))
    archivos = listar_archivos_en_ruta('/ruta', ['.py'])
    mock_listar_archivos.assert_called_once_with('/ruta', ['.py'])
    assert archivos == ['archivo1.py']

def test_generar_reporte(mocker):
    mock_report_generator = MagicMock()
    mock_generar_archivo_salida = mocker.patch.object(mock_report_generator, 'generar_archivo_salida')
    generar_reporte('/ruta', 'modo_prompt', '/project_path', mock_report_generator, ['archivo1.py'], ['.py'])
    mock_generar_archivo_salida.assert_called_once_with('/ruta', 'modo_prompt', ['.py'], '/project_path')
