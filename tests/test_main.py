#AnalizadorDeProyectos/tests/test_main.py
import sys
import os
import subprocess

# Asegúrate de que el directorio raíz esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from setup import check_dependencies
from src.installer_utils import crear_archivo_bat_con_pipenv

@pytest.fixture
def directorio_temporal(tmpdir):
    # Creamos un directorio temporal para las pruebas
    temp_dir = tmpdir.mkdir("temp_dir")
    yield temp_dir
    # Limpiamos el directorio temporal después de cada prueba
    temp_dir.remove(rec=True)

def test_generate_bat_file_with_pipenv(directorio_temporal):
    # Creamos un archivo BAT en el directorio temporal
    ruta_archivo_bat = directorio_temporal.join("test.bat")
    python_executable = sys.executable  # Ruta al ejecutable de Python

    # Llamamos a la función para crear el archivo BAT
    crear_archivo_bat_con_pipenv(directorio_temporal, "test_project")

    # Verificamos que el archivo BAT se haya creado correctamente
    assert ruta_archivo_bat.exists()

def test_limpieza_pantalla(capfd):
    # Simulamos la limpieza de la pantalla
    check_dependencies()

    # Capturamos la salida de la función y verificamos que se haya limpiado la pantalla
    out, _ = capfd.readouterr()
    assert "Todas las dependencias están instaladas." in out
