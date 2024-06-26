#AnalizadorDeProyectos\src\installer_utils.py
from pathlib import Path
from .logs.config_logger import configurar_logging
import winshell
from win32com.client import Dispatch
from pywintypes import com_error

# Configuración del logger
logger = configurar_logging()


def get_project_name():
    """
    Recupera el nombre del proyecto basado en el nombre del directorio principal o un archivo específico.
    """
    try:
        # Obtener el directorio principal del proyecto
        project_dir = Path(__file__).parent.parent.resolve()
        
        # Suponiendo que el nombre del proyecto es el nombre del directorio principal
        project_name = project_dir.name
        logger.debug(f"Nombre del proyecto detectado: {project_name}")
        
        return project_name
    except Exception as e:
        logger.error(f"Error al obtener el nombre del proyecto: {e}")
        return "Unknown_Project"

def verificar_icono(ruta_icono):
    """
    Verifica la existencia del archivo de icono.
    """
    if not ruta_icono.is_file():
        logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
        return False
    return True

def create_shortcut(ruta_archivo_bat, directorio_script, name_proj):
    escritorio = Path(winshell.desktop())
    ruta_acceso_directo = escritorio / f"{name_proj}.lnk"
    ruta_icono = directorio_script / "config" / f"{name_proj}.ico"

    # Llamada a la nueva función para verificar el archivo de icono
    if not verificar_icono(ruta_icono):
        return False

    try:
        shell = Dispatch('WScript.Shell')
        acceso_directo = shell.CreateShortCut(str(ruta_acceso_directo))
        acceso_directo.Targetpath = str(ruta_archivo_bat)
        acceso_directo.WorkingDirectory = str(directorio_script)
        acceso_directo.IconLocation = str(ruta_icono)
        acceso_directo.save()
        logger.debug(f"Acceso directo {'actualizado' if ruta_acceso_directo.exists() else 'creado'} exitosamente.")
        return True
    except com_error as e:
        logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error de COM: {e}", exc_info=True)
        return False
    except OSError as e:
        logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error del sistema operativo: {e}", exc_info=True)
        return False

def crear_archivo_bat_con_pipenv(directorio_script, name_proj):
    ruta_app_py = directorio_script / 'run.py'
    ruta_archivo_bat = directorio_script / f"{name_proj}.bat"

    contenido_bat = f"""
@echo off
echo Verificando entorno virtual de Pipenv...
pipenv --venv
if errorlevel 1 (
   echo Creando entorno virtual...
   pipenv install
   echo Instalando dependencias necesarias...
   pipenv install reportlab
   pipenv install python-dotenv  
) else (
   echo Verificando si 'reportlab' está instalado...
   pipenv run python -c "import reportlab"
   if errorlevel 1 (
      echo 'reportlab' no encontrado, instalando...
      pipenv install reportlab
   )
   REM Chequeo para python-dotenv
   echo Verificando si 'python-dotenv' está instalado...
   pipenv run python -c "import dotenv"
   if errorlevel 1 (
      echo 'python-dotenv' no encontrado, instalando...
      pipenv install python-dotenv
   )
)
echo Ejecutando aplicación...
pipenv run python "{ruta_app_py}"
echo.
pause

"""

    with open(ruta_archivo_bat, 'w') as archivo_bat:
        archivo_bat.write(contenido_bat.strip())
    logger.debug(f"Archivo '{name_proj}.bat' creado exitosamente.")


def main():
    print("iniciando instalador")
    directorio_script = Path(__file__).parent.parent.resolve()
    print (f"directorio_script: {directorio_script}")
    name_proj = get_project_name()
    print (f"name_proj: {name_proj}")
    # Crear archivo BAT
    ruta_archivo_bat = directorio_script / f"{name_proj}.bat"
    print (f"ruta_archivo_bat: {ruta_archivo_bat}")
    if not ruta_archivo_bat.is_file():
        print(f"Creando archivo '{name_proj}.bat'")
        crear_archivo_bat_con_pipenv(directorio_script, name_proj)
    
    create_shortcut(ruta_archivo_bat, directorio_script,name_proj)

