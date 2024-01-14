#installer.py
import subprocess
import os
import sys
from SCR.logs.config_logger import configurar_logging
import winshell
from win32com.client import Dispatch
from packaging import version

logger = configurar_logging()

#installer.py
import subprocess
import os
import sys
from SCR.logs.config_logger import configurar_logging
import winshell
from win32com.client import Dispatch

logger = configurar_logging()

def crear_acceso_directo(ruta_archivo_bat):
    escritorio = winshell.desktop()
    ruta_acceso_directo = os.path.join(escritorio, "AnalizadorDeProyecto.lnk")
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_icono = os.path.join(directorio_script, "config", "AnalizadorDeProyecto.ico")

    if not os.path.isfile(ruta_icono):
        logger.error(f"El archivo de icono en '{ruta_icono}' no existe. Verifique la ubicación y la existencia del icono.")
        return False

    try:
        shell = Dispatch('WScript.Shell')
        if os.path.isfile(ruta_acceso_directo):
            logger.info("El acceso directo ya existe en el escritorio. Actualizando el acceso directo.")
            acceso_directo = shell.CreateShortCut(ruta_acceso_directo)
        else:
            logger.info("Creando un nuevo acceso directo en el escritorio.")
            acceso_directo = shell.CreateShortCut(ruta_acceso_directo)
        
        acceso_directo.Targetpath = ruta_archivo_bat
        acceso_directo.WorkingDirectory = directorio_script
        acceso_directo.IconLocation = ruta_icono  
        acceso_directo.save()
        logger.info("Acceso directo en el escritorio creado/actualizado exitosamente.")
        return True
    except Exception as e:
        logger.error(f"Error al crear/actualizar el acceso directo: {e}", exc_info=True)
        return False

# Resto del código (incluyendo las funciones main, instalar_dependencias, check_archivo_bat, crear_archivo_bat, obtener_version_python, limpieza_pantalla) permanece igual


def main():
    limpieza_pantalla()
    logger.info("Iniciando instalador")
    version_python = obtener_version_python()
    logger.info(f"Versión de Python en uso: {version_python}")
    instalar_dependencias()

    archivo_bat_existente, ruta_archivo_bat = check_archivo_bat()
    if not archivo_bat_existente:
        ruta_archivo_bat = crear_archivo_bat()
    crear_acceso_directo(ruta_archivo_bat)

def instalar_dependencias():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_requirements = os.path.join(directorio_script, 'requirements.txt')

    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        logger.info("Entorno virtual detectado.")
    else:
        logger.warning("No se detectó un entorno virtual activo. Se recomienda activar el entorno virtual antes de continuar.")
        return

    if os.path.isfile(ruta_requirements):
        logger.info("Verificando dependencias...")
        with open(ruta_requirements) as file:
            required_packages = [line.strip() for line in file if line.strip() and not line.startswith('#')]

        for package in required_packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True, text=True, check=True)
                logger.info(f"Instalado o actualizado: {package}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Error al instalar la dependencia {package}: {e.output}")
                
        logger.info("Verificación y actualización de dependencias completada.")
    else:
        logger.warning("Archivo 'requirements.txt' no encontrado. No se instalaron dependencias adicionales.")

def check_archivo_bat():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo_bat = os.path.join(directorio_script, 'AnalizadorDeProyecto.bat')

    # Verificar si el archivo .bat existe y es válido
    if os.path.isfile(ruta_archivo_bat):
        try:
            with open(ruta_archivo_bat, 'r') as archivo:
                contenido = archivo.read()
            # Verificar si el contenido del archivo .bat es el esperado
            if "AnalizadorDeProyecto.py" not in contenido:
                logger.info("El archivo 'AnalizadorDeProyecto.bat' existente no es válido. Se creará uno nuevo.")
                return False, ruta_archivo_bat
            logger.info("'AnalizadorDeProyecto.bat' ya está instalado y es válido.")
            return True, ruta_archivo_bat
        except Exception as e:
            logger.error(f"Error al leer 'AnalizadorDeProyecto.bat': {e}")
            return False, ruta_archivo_bat
    else:
        logger.info("'AnalizadorDeProyecto.bat' no está instalado.")
        return False, ruta_archivo_bat

def crear_archivo_bat():
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    ruta_entorno_virtual = os.path.join(directorio_script, 'analizador_env')

    if not os.path.exists(ruta_entorno_virtual):
        logger.error(f"El entorno virtual en '{ruta_entorno_virtual}' no existe. Crear el entorno virtual antes de ejecutar este script.")
        return None

    ruta_main_py = os.path.join(directorio_script, 'SCR', 'main.py')
    if not os.path.isfile(ruta_main_py):
        logger.error(f"El archivo 'main.py' no existe en '{ruta_main_py}'. Verifique la ubicación del archivo.")
        return None

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
            "\"%PYTHON_EXEC%\" \"" + ruta_main_py + "\"\n"
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
    try:
        # Para Windows
        if os.name == 'nt':
            os.system('cls')
        # Para Unix y MacOS (posix)
        else:
            os.system('clear')
        logger.info("Pantalla limpiada.")
    except Exception as e:
        logger.error(f"Error al limpiar la pantalla: {e}")

if __name__ == "__main__":
    main()
