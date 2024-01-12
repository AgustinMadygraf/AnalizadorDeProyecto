import subprocess
import os
import sys
from SCR.utilidades_sistema import obtener_version_python, limpieza_pantalla
from SCR.logs.config_logger import configurar_logging



logger = configurar_logging()

def main():
    limpieza_pantalla()
    logger.info("Iniciando instalador")
    version_python = obtener_version_python()
    logger.info(f"Versión de Python en uso: {version_python}")
    if not check_archivo_bat():
        crear_archivo_bat()
    instalar_dependencias()


def instalar_dependencias():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_requirements = os.path.join(directorio_script, 'requirements.txt')
    if os.path.isfile(ruta_requirements):
        logger.info("Verificando dependencias...")
        with open(ruta_requirements) as file:
            required_packages = [line.strip() for line in file if line.strip() and not line.startswith('#')]
        
        installed_packages = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True).stdout
        install_needed = False

        for package in required_packages:
            if package.split("==")[0].lower() not in installed_packages.lower():
                install_needed = True
                break

        if install_needed:
            logger.info("Instalando dependencias...")
            resultado = subprocess.run([sys.executable, "-m", "pip", "install", "-r", ruta_requirements], capture_output=True, text=True)
            if resultado.returncode == 0:
                logger.info("Dependencias instaladas.")
            else:
                logger.error(f"Error al instalar dependencias: {resultado.stderr}")
        else:
            logger.info("Todas las dependencias ya están instaladas.")
    else:
        logger.warning("Archivo 'requirements.txt' no encontrado. No se instalaron dependencias adicionales.")

def check_archivo_bat():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_bat = os.path.join(directorio_script, '..\\AnalizadorDeProyecto.bat')
    if os.path.isfile(ruta_archivo_bat):
        logger.info("\n'AnalizadorDeProyecto.bat' ya está instalado.\n")
        return True
    else:
        logger.warning("\n'AnalizadorDeProyecto.bat' no está instalado.\n")
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

        ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat)
        logger.info("Archivo 'AnalizadorDeProyecto.bat' creado exitosamente.")
    except Exception as e:
        logger.error(f"Error al crear el archivo .bat: {e}")


if __name__ == "__main__":
    main()
