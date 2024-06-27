# tests/test_report_generator.py
import pytest
from src.models.report_generator import ReportGenerator
from unittest.mock import patch, mock_open

@pytest.fixture
def report_generator():
    return ReportGenerator("C:\\AppServ\\www\\AnalizadorDeProyecto")

def test_generar_archivo_salida(report_generator, mocker):
    mocker.patch("builtins.open", mock_open(read_data="content"))
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("src.file_operations.listar_archivos", return_value=([], []))
    mocker.patch.object(report_generator, 'generar_nombre_archivo_salida', return_value="output.md")
    mocker.patch.object(report_generator, 'escribir_archivo_salida', return_value=True)
    mocker.patch("src.file_utilities.copiar_contenido_al_portapapeles")

    result = report_generator.generar_archivo_salida("path", "modo_prompt", [], "ruta_archivos")
    assert result == "output.md"

def test_preparar_contenido_salida(report_generator, mocker):
    mocker.patch.object(report_generator.file_manager, 'read_and_validate_file', return_value="Prompt content")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mock_open(read_data="TODO content"))

    contenido = report_generator.preparar_contenido_salida([], "modo_prompt", [], "path", "ruta_archivos", [])
    assert "Prompt content" in contenido
    assert "TODO content" in contenido
