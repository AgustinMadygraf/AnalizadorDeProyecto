import logging

def configurar_logging():
    logging.basicConfig(filename='proyecto.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
