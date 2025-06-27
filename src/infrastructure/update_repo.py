# src/infrastructure/update_repo.py
import os
import subprocess
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
        try:
            result = subprocess.run(['git', 'status'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git status: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git status: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error al realizar git status: {e}")

    def git_restore(self):
        try:
            result = subprocess.run(['git', 'restore', '--staged', '.'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git restore (staged): {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git restore (staged): {result.stderr}")

            result = subprocess.run(['git', 'restore', '.'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git restore (local): {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git restore (local): {result.stderr}")

            result = subprocess.run(['git', 'clean', '-fd'], capture_output=True, text=True)
            self.logger.debug(f"Salida de git clean: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git clean: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error al restaurar el repositorio: {e}")
