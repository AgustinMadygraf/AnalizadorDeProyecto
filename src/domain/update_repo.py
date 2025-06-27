#AnalizadorDeProyecto/src/domain/update_repo.py
import os
import subprocess
import logging
from src.logs.config_logger import LoggerConfigurator

class RepoUpdater:
    def __init__(self, repo_path):
        """
        Inicializa la clase RepoUpdater con la ruta del repositorio.

        :param repo_path: Ruta del repositorio.
        """
        self.repo_path = repo_path
        self.logger = LoggerConfigurator().get_logger()

    def git_status(self):
        """
        Verifica el estado del repositorio.
        """
        try:
            # Ejecuta el comando git status
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git status: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git status: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error al realizar git status: {e}")

    def git_restore(self):
        """
        Restaura los cambios locales no deseados y elimina archivos no rastreados.
        """
        try:
            # Ejecuta el comando git restore para descartar cambios locales
            result = subprocess.run(['git', 'restore', '--staged', '.'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git restore (staged): {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git restore (staged): {result.stderr}")

            result = subprocess.run(['git', 'restore', '.'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git restore (local): {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git restore (local): {result.stderr}")

            # Ejecuta el comando git clean para eliminar archivos no rastreados
            result = subprocess.run(['git', 'clean', '-fd'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git clean: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git clean: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error al realizar git restore/git clean: {e}")

    def git_pull(self):
        """
        Realiza un git pull en el repositorio especificado en repo_path.
        """
        try:
            # Cambia al directorio del repositorio
            os.chdir(self.repo_path)
            result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git pull: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git pull: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error al realizar git pull: {e}")
