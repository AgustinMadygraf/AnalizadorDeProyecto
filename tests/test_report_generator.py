# tests/domain/test_report_generator.py
import pytest
from src.domain.report_generator import ReportGenerator
from unittest.mock import patch, mock_open

@pytest.fixture
def report_generator():
    # Mock de puertos/adaptadores para pruebas
    class DummyPort:
        def read_and_validate_file(self, *a, **kw): return "Prompt content"
        def process_file(self, *a, **kw): return "Archivo"
        def asegurar_directorio_docs(self, *a, **kw): pass
        def listar_archivos(self, *a, **kw): return ([], [])
        def copiar_contenido_al_portapapeles(self, *a, **kw): pass
        def debug(self, *a, **kw): pass
        def info(self, *a, **kw): pass
        def warning(self, *a, **kw): pass
        def error(self, *a, **kw): pass
    dummy = DummyPort()
    return ReportGenerator(
        "C:\\AppServ\\www\\AnalizadorDeProyecto",
        dummy, dummy, dummy, dummy, dummy
    )

def test_generar_archivo_salida(report_generator, mocker):
    mocker.patch("builtins.open", mock_open(read_data="content"))
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("src.infrastructure.file_operations_adapter.listar_archivos", return_value=([], []))
    mocker.patch.object(report_generator, 'generar_nombre_archivo_salida', return_value="output.md")
    mocker.patch.object(report_generator, 'escribir_archivo_salida', return_value=True)
    mocker.patch("src.infrastructure.file_utilities.copiar_contenido_al_portapapeles")

    result = report_generator.generar_archivo_salida("path", "modo_prompt", [], "ruta_archivos", True)
    assert result == "output.md"

def test_preparar_contenido_salida(report_generator, mocker):
    mocker.patch.object(report_generator.file_manager, 'read_and_validate_file', return_value="Prompt content")
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("builtins.open", mock_open(read_data="TODO content"))

    contenido = report_generator.preparar_contenido_salida([], "modo_prompt", [], "path", "ruta_archivos", [])
    assert "Prompt content" in contenido
    assert "TODO content" in contenido
