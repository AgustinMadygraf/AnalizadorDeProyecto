# src/report_generator.py

from models.report_generator import ReportGenerator

# Ahora puedes instanciar y usar ReportGenerator donde sea necesario en este archivo.
project_path = "C:\\AppServ\\www\\AnalizadorDeProyecto"
report_generator = ReportGenerator(project_path)

# Usar la instancia del generador de reportes para llamar al método.
report_generator.generar_archivo_salida("ruta", "modo_prompt", ["extensiones_permitidas"], "ruta_archivos", incluir_todo=True)
