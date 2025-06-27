# src/common/validation.py
"""
Funciones centralizadas para validación de entradas y manejo de errores de usuario.
"""

def validate_menu_option(option: str, valid_options: list) -> bool:
    """Valida si la opción ingresada es válida."""
    return option in valid_options

def get_error_message(key: str, lang: dict) -> str:
    """Obtiene el mensaje de error traducido."""
    return lang.get(key, "[ERROR] Error desconocido.")
