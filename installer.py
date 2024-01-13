import subprocess
import os
import sys
from SCR.logs.config_logger import configurar_logging
import os
import winshell
from win32com.client import Dispatch

logger = configurar_logging()

def crear_acceso_directo(ruta_archivo_bat):
    escritorio = winshell.desktop()
    print("\nescritorio: ",escritorio,"\n\n")
    ruta_acceso_directo = os.path.join(escritorio, "AnalizadorDeProyecto.lnk")
    print("ruta_acceso_directo: ",ruta_acceso_directo,"\n\n")
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    print("directorio_script: ",directorio_script,"\n\n")
    print("ruta_archivo_bat: ",ruta_archivo_bat,"\n\n")
    ruta_icono = os.path.join(directorio_script, "config\AnalizadorDeProyecto.ico")

    try:
        if not os.path.isfile(ruta_acceso_directo):
            shell = Dispatch('WScript.Shell')
            acceso_directo = shell.CreateShortCut(ruta_acceso_directo)
            acceso_directo.Targetpath = ruta_archivo_bat
            acceso_directo.WorkingDirectory = directorio_script
            acceso_directo.IconLocation = ruta_icono  
            acceso_directo.save()

            logger.info("Acceso directo en el escritorio creado.")
        else:
            logger.info("El acceso directo ya existe en el escritorio.")
    except Exception as e:
        logger.error(f"Error al crear el acceso directo: {e}")

def main():
    limpieza_pantalla()
    logger.info("Iniciando instalador")
    version_python = obtener_version_python()
    logger.info(f"Versión de Python en uso: {version_python}")
    # Resto de tu código...
    archivo_bat_existente, ruta_archivo_bat = check_archivo_bat()
    if not archivo_bat_existente:
        ruta_archivo_bat = crear_archivo_bat()
    instalar_dependencias()
    crear_acceso_directo(ruta_archivo_bat)

def instalar_dependencias():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_requirements = os.path.join(directorio_script, 'requirements.txt')
    
    # Verifica si se está ejecutando dentro de un entorno virtual
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        logger.info("Entorno virtual detectado.")
    else:
        logger.warning("No se detectó un entorno virtual activo. Se recomienda activar el entorno virtual antes de continuar.")
        return

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
    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')
    if os.path.isfile(ruta_archivo_bat):
        logger.info("'AnalizadorDeProyecto.bat' ya está instalado.")
        return True, ruta_archivo_bat
    else:
        logger.info("'AnalizadorDeProyecto.bat' no está instalado.")
        return False, ruta_archivo_bat

def crear_archivo_bat():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_entorno_virtual = os.path.join(directorio_script, 'analizador_env')
    ruta_python_executable = os.path.join(ruta_entorno_virtual, 'Scripts', 'python.exe')
    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')

    try:
        contenido_bat = (
            "@echo off\n"
            "setlocal\n"
            "\n"
            "set \"SCRIPT_DIR=%~dp0\"\n"
            "set \"VENV_DIR=" + ruta_entorno_virtual + "\"\n"
            "set \"PYTHON_EXEC=" + ruta_python_executable + "\"\n"
            "\n"
            "if not exist \"%PYTHON_EXEC%\" (\n"
            "    echo No se encontró el ejecutable de Python en el entorno virtual. Asegúrese de que el entorno virtual está activo.\n"
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
            "    echo El script de Python falló. Verifique las dependencias y la versión de Python en el entorno virtual.\n"
            "    pause\n"
            "    exit /b\n"
            ")\n"
            "\n"
            "pause\n"
            "endlocal\n"
        )

        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat)
        logger.info("Archivo 'AnalizadorDeProyecto.bat' creado exitosamente.")
    except Exception as e:
        logger.error(f"Error al crear el archivo .bat: {e}")
    return ruta_archivo_bat

def obtener_version_python():
    return sys.version


def limpieza_pantalla():
    logger.info("Limpiando pantalla.")
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == "__main__":
    main()
