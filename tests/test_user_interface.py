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

def test_menu_0():
    ui = UserInterface()
    
    with patch('builtins.input', side_effect=['/ruta/de/prueba']):
        resultado = ui.menu_0()
        assert resultado == '/ruta/de/prueba'

def test_menu_1():
    ui = UserInterface()
    opciones = {
        '0': 'config\\prompt_0.md',
        '1': 'config\\prompt_1.md',
        '2': 'config\\prompt_2.md',
        '3': 'config\\prompt_3.md',
        '4': 'config\\prompt_4.md',
        '5': 'config\\prompt_5.md' 
    }
    
    with patch('builtins.input', side_effect=['1']):
        resultado = ui.menu_1()
        assert resultado == 'config\\prompt_1.md'
