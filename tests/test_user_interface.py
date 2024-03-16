#AnalizadorDeProyecto/tests/test_user_interface.py
import pytest
from src.user_interface import menu_0, menu_1

def test_menu_0_input(monkeypatch):
    """
    Test para verificar que menu_0 maneja correctamente la entrada del usuario.
    """
    user_input = "C:\\test\\path"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert menu_0() == user_input, "menu_0 debería retornar la entrada del usuario"

def test_menu_1_selection(monkeypatch):
    """
    Test para verificar que menu_1 retorna la opción correcta basada en la entrada del usuario.
    """
    # Suponemos que el usuario elige la opción 1
    monkeypatch.setattr('builtins.input', lambda _: '1')
    assert menu_1() == 'config\\prompt_upd_0.md', "menu_1 debería retornar el path correcto para la opción 1"

# Agrega más tests según sea necesario para cubrir las funciones en user_interface.py
