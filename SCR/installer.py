from logs.config_logger import configurar_logging
import os
import sys

logger = configurar_logging()

def main():
    print("Iniciando instalador")
    if not check_archivo_bat():
        crear_archivo_bat()
    instalar_dependencias()

def instalar_dependencias():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_requirements = os.path.join(directorio_script, '..', 'requirements.txt')
    if os.path.isfile(ruta_requirements):
        print("Instalando dependencias...")
        os.system(f"\"{sys.executable}\" -m pip install -r \"{ruta_requirements}\"")
        print("Dependencias instaladas.")
    else:
        print("Archivo 'requirements.txt' no encontrado. No se instalaron dependencias adicionales.")

def check_archivo_bat():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_bat = os.path.join(directorio_script, '..\AnalizadorDeProyecto.bat')
    if os.path.isfile(ruta_archivo_bat):
        print("'AnalizadorDeProyecto.bat' ya está instalado.")
        return True
    else:
        print("'AnalizadorDeProyecto.bat' no está instalado.")
        return False

def crear_archivo_bat():
    try:
        python_executable = sys.executable
        directorio_script = os.path.dirname(os.path.abspath(__file__))

        contenido_bat = (
            "@echo off\n"
            "setlocal\n"
            "\n"
            "set \"SCRIPT_DIR=%~dp0\"\n"
            "set \"PYTHON_EXEC=" + python_executable + "\"\n"
            "\n"
            "if not exist \"%PYTHON_EXEC%\" (\n"
            "    echo No se encontró el ejecutable de Python. Asegúrese de que Python está instalado.\n"
            "    pause\n"
            "    exit /b\n"
            ")\n"
            "\n"
            "cd /d \"%SCRIPT_DIR%\"\n"
            "if errorlevel 1 (\n"
            "    echo No se pudo cambiar al directorio del script. Verifique la ubicación de 'AnalizadorDeProyecto.bat'.\n"
            "    pause\n"
            "    exit /b\n"
            ")\n"
            "\n"
            "\"%PYTHON_EXEC%\" SCR\\main.py\n"
            "if errorlevel 1 (\n"
            "    echo El script de Python falló. Verifique las dependencias y la versión de Python.\n"
            "    pause\n"
            "    exit /b\n"
            ")\n"
            "\n"
            "pause\n"
            "endlocal\n"
        )

        ruta_archivo_bat = os.path.join(directorio_script, '..\\AnalizadorDeProyecto.bat')
        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat)
        print("Archivo 'AnalizadorDeProyecto.bat' creado exitosamente.")
    except Exception as e:
        logger.error(f"Error al crear el archivo .bat: {e}")


if __name__ == "__main__":
    main()
