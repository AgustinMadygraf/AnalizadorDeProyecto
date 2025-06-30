# src/common/validation.py
"""
Funciones centralizadas para validación de entradas y manejo de errores de usuario.
"""

# TODO: Revisar posible código muerto (vulture): función 'validate_menu_option' reportada como sin uso
def validate_menu_option(option: str, valid_options: list) -> bool:
    """Valida si la opción ingresada es válida."""
    return option in valid_options

# TODO: Revisar posible código muerto (vulture): función 'get_error_message' reportada como sin uso
def get_error_message(key: str, lang: dict) -> str:
    """Obtiene el mensaje de error traducido."""
    return lang.get(key, "[ERROR] Error desconocido.")
