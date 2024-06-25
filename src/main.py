# src/main.py

import logging
from src.controllers.gestor_archivos import GestorArchivos
from src.controllers.analizador_proyecto import AnalizadorDeProyecto
from src.views.interfaz_usuario import InterfazUsuario
from src.config.config_logger import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)

def main():
    interfaz = InterfazUsuario()
    gestor = GestorArchivos('ruta/al/proyecto')
    analizador = AnalizadorDeProyecto('ruta/al/proyecto')

    while True:
        opcion = interfaz.mostrar_menu()
        if opcion == '1':
            archivos = gestor.obtener_archivos()
            interfaz.mostrar_archivos(archivos)
        elif opcion == '2':
            analizador.analizar()
            reporte = analizador.generar_reporte()
            interfaz.mostrar_reporte(reporte)
        elif opcion == '3':
            break
        else:
            logger.warning("Opción no válida")

if __name__ == "__main__":
    main()
