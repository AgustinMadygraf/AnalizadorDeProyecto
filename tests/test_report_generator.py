# AnalizadorDeProeyctos/src/test_report_generator.py
import pytest
from unittest.mock import patch, mock_open
from src.report_generator import (
    generar_archivo_salida,
    formatear_archivo_salida,
    preparar_contenido_salida,
    construir_contenido_archivos_seleccionados,
    escribir_archivo_salida
)

# Prueba para generar el archivo de salida
@patch("src.report_generator.listar_archivos", return_value=(["archivo1.py"], ["estructura"]))
@patch("src.report_generator.asegurar_directorio_docs")
@patch("src.report_generator.preparar_contenido_salida", return_value="contenido")
@patch("src.report_generator.escribir_archivo_salida", return_value=True)
@patch("src.report_generator.copiar_contenido_al_portapapeles")
def test_generar_archivo_salida(mock_copiar, mock_escribir, mock_preparar, mock_asegurar, mock_listar):
    path = "test_path"
    modo_prompt = "config\\prompt_1.md"
    extensiones_permitidas = [".py", ".txt"]
    ruta_archivos = "test_path"
    resultado = generar_archivo_salida(path, modo_prompt, extensiones_permitidas, ruta_archivos)
    assert resultado == "test_path\\docs\\00-Prompt-for-ProjectAnalysis.md"

# Prueba para formatear el archivo de salida
@patch("builtins.open", new_callable=mock_open)
def test_formatear_archivo_salida(mock_file):
    formatear_archivo_salida("test_path\\test_file.md")
    mock_file.assert_called_once_with("test_path\\test_file.md", 'w', encoding='utf-8')

# Prueba para preparar el contenido de salida
@patch("src.report_generator.read_and_validate_file", return_value="contenido de prompt")
def test_preparar_contenido_salida(mock_read):
    estructura = ["estructura"]
    modo_prompt = "config\\prompt_1.md"
    archivos_seleccionados = ["archivo1.py"]
    path = "test_path"
    ruta_archivo = "test_path"
    extensiones_permitidas = [".py", ".txt"]
    contenido = preparar_contenido_salida(estructura, modo_prompt, archivos_seleccionados, path, ruta_archivo, extensiones_permitidas)
    assert "contenido de prompt" in contenido

# Prueba para construir el contenido de archivos seleccionados
@patch("src.report_generator.read_and_validate_file", return_value="contenido del archivo")
def test_construir_contenido_archivos_seleccionados(mock_read):
    archivos_seleccionados = ["archivo1.py"]
    extensiones_permitidas = [".py", ".txt"]
    contenido = construir_contenido_archivos_seleccionados(archivos_seleccionados, extensiones_permitidas)
    assert "contenido del archivo" in contenido

# Prueba para escribir el contenido en el archivo de salida
@patch("builtins.open", new_callable=mock_open)
def test_escribir_archivo_salida(mock_file):
    nombre_archivo = "test_path\\test_file.md"
    contenido = "contenido"
    resultado = escribir_archivo_salida(nombre_archivo, contenido)
    assert resultado is True
    mock_file.assert_called_once_with(nombre_archivo, 'w', encoding='utf-8')
    handle = mock_file()
    handle.write.assert_called_once_with(contenido)
