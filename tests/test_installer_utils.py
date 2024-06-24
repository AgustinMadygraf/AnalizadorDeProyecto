# AnalizadorDeProeyctos/src/test_installer_utils.py
import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.installer_utils import (
    get_project_name,
    create_shortcut,
    crear_archivo_bat_con_pipenv
)

# Prueba para obtener el nombre del proyecto
@patch("src.installer_utils.Path")
def test_get_project_name(mock_path):
    mock_path.return_value.parent.parent.resolve.return_value.name = "AnalizadorDeProyecto"
    nombre_proyecto = get_project_name()
    assert nombre_proyecto == "AnalizadorDeProyecto"

# Prueba para crear un acceso directo
@patch("src.installer_utils.winshell.desktop", return_value="C:\\Users\\usuario\\Desktop")
@patch("src.installer_utils.Dispatch")
def test_create_shortcut(mock_dispatch, mock_desktop):
    ruta_archivo_bat = Path("C:\\AppServ\\www\\AnalizadorDeProyecto\\AnalizadorDeProyecto.bat")
    directorio_script = Path("C:\\AppServ\\www\\AnalizadorDeProyecto")
    nombre_proyecto = "AnalizadorDeProyecto"
    mock_shell = MagicMock()
    mock_dispatch.return_value = mock_shell
    mock_shortcut = mock_shell.CreateShortCut.return_value

    result = create_shortcut(ruta_archivo_bat, directorio_script, nombre_proyecto)

    assert result is True
    mock_shortcut.Targetpath = str(ruta_archivo_bat)
    mock_shortcut.WorkingDirectory = str(directorio_script)
    mock_shortcut.IconLocation = str(directorio_script / "config" / f"{nombre_proyecto}.ico")
    mock_shortcut.save.assert_called_once()

# Prueba para crear un archivo BAT con pipenv
@patch("builtins.open", new_callable=MagicMock)
def test_crear_archivo_bat_con_pipenv(mock_open):
    directorio_script = Path("C:\\AppServ\\www\\AnalizadorDeProyecto")
    nombre_proyecto = "AnalizadorDeProyecto"
    crear_archivo_bat_con_pipenv(directorio_script, nombre_proyecto)
    ruta_archivo_bat = directorio_script / f"{nombre_proyecto}.bat"

    mock_open.assert_called_once_with(ruta_archivo_bat, 'w')
    handle = mock_open()
    handle.write.assert_called_once()
