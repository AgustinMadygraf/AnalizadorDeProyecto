# AnalizadorDeProeyctos/src/test_user_interface.py
import pytest
from unittest.mock import patch, MagicMock
from src.user_interface import menu_0, solicitar_opcion, menu_1

# Prueba para la función menu_0
@patch("builtins.input", return_value="test_path")
def test_menu_0(mock_input):
    ruta = menu_0()
    assert ruta == "test_path"

# Prueba para la función solicitar_opcion
@patch("builtins.input", side_effect=["1", "2"])
def test_solicitar_opcion(mock_input):
    mensaje = "Seleccione una opción:"
    opciones = {1: "Opción 1", 2: "Opción 2"}
    opcion = solicitar_opcion(mensaje, opciones)
    assert opcion == "Opción 1"
    opcion = solicitar_opcion(mensaje, opciones)
    assert opcion == "Opción 2"

# Prueba para la función menu_1
@patch("builtins.input", return_value="1")
def test_menu_1(mock_input):
    opcion = menu_1()
    assert opcion == "config\\prompt_1.md"
