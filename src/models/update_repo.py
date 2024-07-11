#AnalizadorDeProyecto/src/models/update_repo.py
import os
import subprocess
import logging

class RepoUpdater:
    def __init__(self, repo_path):
        """
        Inicializa la clase RepoUpdater con la ruta del repositorio.

        :param repo_path: Ruta del repositorio.
        """
        self.repo_path = repo_path
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Configura el logger para la clase RepoUpdater.

        :return: Objeto logger configurado.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def git_pull(self):
        """
        Realiza un git pull en el repositorio especificado en repo_path.
        """
        try:
            # Cambia al directorio del repositorio
            os.chdir(self.repo_path)
            self.logger.debug(f"Directorio cambiado a {self.repo_path}")

            # Ejecuta el comando git pull
            result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
            
            # Imprime la salida del comando git pull
            self.logger.debug(f"Salida de git pull: {result.stdout}")
            if result.stderr:
                self.logger.error(f"Error en git pull: {result.stderr}")
        except Exception as e:
            self.logger.error(f"Error al realizar git pull: {e}")

    def run(self):
        """
        Ejecuta el proceso de actualización del repositorio.
        """
        self.logger.debug("Iniciando el proceso de git pull")
        self.git_pull()
        
if __name__ == "__main__":
    repo_path = 'C:\AppServ\www\AnalizadorDeProyecto'
    updater = RepoUpdater(repo_path)
    updater.run()
