# tests/test_user_interface.py
import pytest
from unittest.mock import patch
from src.models.user_interface import UserInterface

def test_solicitar_opcion_valida():
    ui = UserInterface()
    mensaje = "Seleccione una opción:"
    opciones = {1: 'opcion1', 2: 'opcion2'}
    
    with patch('builtins.input', side_effect=['1']):
        resultado = ui.solicitar_opcion(mensaje, opciones)
        assert resultado == 'opcion1'

def test_solicitar_opcion_invalida():
    ui = UserInterface()
    mensaje = "Seleccione una opción:"
    opciones = {1: 'opcion1', 2: 'opcion2'}
    
    with patch('builtins.input', side_effect=['3', '2']):
        resultado = ui.solicitar_opcion(mensaje, opciones)
        assert resultado == 'opcion2'
