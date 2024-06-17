#AnalizadorDeProyecto\tests\test_main.py
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

import setup
import pytest



# Fixture para preparar el entorno de pruebas
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
    python_executable = "/usr/bin/python3"  # Ruta al ejecutable de Python
    setup.generate_bat_file_with_pipenv(str(directorio_temporal), python_executable)

    # Verificamos que el archivo BAT se haya creado correctamente
    assert ruta_archivo_bat.exists()

def test_limpieza_pantalla(capfd):
    # Simulamos la limpieza de la pantalla
    setup.limpieza_pantalla()

    # Capturamos la salida de la función y verificamos que se haya limpiado la pantalla
    out, _ = capfd.readouterr()
    assert "Pantalla limpiada." in out
