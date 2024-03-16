import pytest
import installer

# Fixture para preparar el entorno de pruebas
@pytest.fixture
def directorio_temporal(tmpdir):
    # Creamos un directorio temporal para las pruebas
    temp_dir = tmpdir.mkdir("temp_dir")
    yield temp_dir
    # Limpiamos el directorio temporal después de cada prueba
    temp_dir.remove(rec=True)

def test_crear_archivo_bat_con_pipenv(directorio_temporal):
    # Creamos un archivo BAT en el directorio temporal
    ruta_archivo_bat = directorio_temporal.join("test.bat")
    python_executable = "/usr/bin/python3"  # Ruta al ejecutable de Python
    installer.crear_archivo_bat_con_pipenv(str(directorio_temporal), python_executable)

    # Verificamos que el archivo BAT se haya creado correctamente
    assert ruta_archivo_bat.exists()

def test_limpieza_pantalla(capfd):
    # Simulamos la limpieza de la pantalla
    installer.limpieza_pantalla()

    # Capturamos la salida de la función y verificamos que se haya limpiado la pantalla
    out, _ = capfd.readouterr()
    assert "Pantalla limpiada." in out
