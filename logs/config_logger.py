import logging
from logging.handlers import RotatingFileHandler

def configurar_logging(
        filename='proyecto.log',
        file_level=logging.DEBUG,  # Nivel de registro para el archivo
        console_level=logging.INFO,  # Nivel de registro para la consola
        format='%(asctime)s - %(levelname)s - %(module)s: %(message)s',
        maxBytes=10485760,  # 10MB
        backupCount=5
    ):
    """
    Configura el logging para el proyecto.

    Args:
        filename (str): Nombre del archivo de log.
        file_level (int): Nivel de logging para el archivo.
        console_level (int): Nivel de logging para la consola.
        format (str): Formato de los mensajes de log.
        maxBytes (int): Tamaño máximo del archivo de log en bytes antes de la rotación.
        backupCount (int): Número de archivos de backup a mantener.
    """

    # Creación del formateador
    formatter = logging.Formatter(format)

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    # Configuración del logger raíz
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
