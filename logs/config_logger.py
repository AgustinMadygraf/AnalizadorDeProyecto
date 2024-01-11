import logging
from logging.handlers import RotatingFileHandler

def configurar_logging(
        filename='proyecto.log',
        level=logging.DEBUG,  # Establecer el nivel de registro en DEBUG
        format='%(asctime)s - %(levelname)s - %(module)s: %(message)s',
        maxBytes=10485760,  # 10MB
        backupCount=5
    ):
    """
    Configura el logging para el proyecto.

    Args:
        filename (str): Nombre del archivo de log.
        level (int): Nivel de logging.
        format (str): Formato de los mensajes de log.
        maxBytes (int): Tamaño máximo del archivo de log en bytes antes de la rotación.
        backupCount (int): Número de archivos de backup a mantener.
    """

    # Creación del formateador
    formatter = logging.Formatter(format)

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configuración del logger
    logger = logging.getLogger()  # Obtener el logger raíz
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # Configuración del logger
    logger = logging.getLogger()  # Obtener el logger raíz
    logger.setLevel(logging.INFO)  # Establecer el nivel de registro en INFO para la consola
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# Ejemplo de uso
# configurar_logging(level=logging.INFO)
