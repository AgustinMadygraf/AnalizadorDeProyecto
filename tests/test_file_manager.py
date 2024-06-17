#AnalizadorDeProyecto\tests\test_file_manager.py
import os
import sys
import pytest
ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ruta_proyecto)
from src.file_manager import read_file

# Preparación de un entorno de prueba: Creación de archivos de prueba
@pytest.fixture(scope="module")
def crear_archivos_prueba(tmp_path_factory):
    base_temp_dir = tmp_path_factory.mktemp("data")
    # Crear archivos de prueba con diferentes extensiones y contenidos
    archivos_prueba = {
        "texto_permitido.txt": "Contenido del archivo de texto.",
        "imagen_no_permitida.jpg": "Esto debería fallar.",
        "script_python.py": "print('Hola Mundo')",
        "documento_grande.md": "a" * 10241  # Mayor que el límite de 10KB
    }
    for nombre, contenido in archivos_prueba.items():
        ruta = base_temp_dir / nombre
        ruta.write_text(contenido, encoding='utf-8')

    return base_temp_dir

# Prueba: Lectura de archivo permitido
def test_read_file_permitido(crear_archivos_prueba):
    ruta_archivo = crear_archivos_prueba / "texto_permitido.txt"
    contenido = read_file(str(ruta_archivo))
    assert contenido == "Contenido del archivo de texto."

# Prueba: Rechazo de extensión no permitida
def test_extension_no_permitida(crear_archivos_prueba):
    ruta_archivo = crear_archivos_prueba / "imagen_no_permitida.jpg"
    contenido = read_file(str(ruta_archivo))
    assert contenido is None

# Prueba: Lectura de script de Python permitido
def test_leer_script_python(crear_archivos_prueba):
    ruta_archivo = crear_archivos_prueba / "script_python.py"
    contenido = read_file(str(ruta_archivo))
    assert contenido == "print('Hola Mundo')"

# Prueba: Rechazo de archivo por tamaño
def test_documento_grande_rechazado(crear_archivos_prueba):
    ruta_archivo = crear_archivos_prueba / "documento_grande.md"
    contenido = read_file(str(ruta_archivo))
    assert contenido is None

# Asegúrate de ejecutar estas pruebas en un entorno donde `src.file_manager` sea accesible.
# Puede que necesites ajustar las rutas de importación según la estructura de tu proyecto.
