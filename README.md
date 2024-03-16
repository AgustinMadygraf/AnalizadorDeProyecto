# AnalizadorDeProyecto

## Descripción
El `AnalizadorDeProyecto` es una herramienta avanzada en Python, diseñada para analizar, documentar y mejorar la estructura de proyectos de software. Ideal para la gestión y mantenimiento del código, esta herramienta ofrece funciones mejoradas de verificación, instalación de dependencias, enumeración avanzada de archivos por extensión y generación de informes detallados sobre la arquitectura del proyecto con capacidades de visualización.

## Versión de Python
El `AnalizadorDeProyecto` ha sido actualizado para ser compatible y ha sido testeado con Python 3.9, asegurando una mayor eficiencia y compatibilidad con las versiones más recientes. *Nota: Se recomienda verificar periódicamente las actualizaciones de Python y las dependencias para mantener la compatibilidad y seguridad.*

## Instalación y configuración del entorno de desarrollo

Este proyecto soporta `pipenv` para la gestión de dependencias y el entorno virtual, y también ofrece soporte para `pip` y un entorno virtual estándar, facilitando así la configuración del entorno de desarrollo y promoviendo prácticas de desarrollo consistentes para una amplia gama de usuarios.

### Configuración usando `pipenv`

1. **Instalar `pipenv`**:
   Asegúrate de tener `pipenv` instalado en tu sistema. Si no, puedes instalarlo con:
   ```bash
   pip install pipenv
   ```

2. **Clonar el repositorio del proyecto**:
   ```bash
   git clone https://github.com/AgustinMadygraf/AnalizadorDeProyecto
   cd <DIRECTORIO_DEL_PROYECTO>
   ```

3. **Instalar las dependencias y activar el entorno virtual**:
   ```bash
   pipenv install
   pipenv shell
   ```

4. **Ejecutar la aplicación**:
   ```bash
   python src/main.py
   ```

### Configuración usando `pip` y un entorno virtual estándar

1. **Clonar el repositorio del proyecto**:
   Sigue los mismos pasos que en la sección anterior.

2. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   - En Windows: `.\venv\Scripts\activate`
   - En Unix o MacOS: `source venv/bin/activate`

4. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar la aplicación**:
   ```bash
   python src/main.py
   ```

## Preguntas Frecuentes (FAQ)

### ¿Cómo puedo empezar a usar el AnalizadorDeProyecto?
Dependiendo del método de instalación elegido, asegúrate de que el entorno virtual esté activo (`pipenv shell` para pipenv o activar el entorno virtual estándar) y luego ejecuta `src/main.py` en la raíz de tu proyecto para comenzar el análisis.

### ¿En qué sistemas operativos funciona el AnalizadorDeProyecto?
El proyecto se ha actualizado para asegurar la compatibilidad con sistemas operativos que soporten Python 3.9, mejorando así nuestra cobertura en distintas plataformas.

### ¿Puedo contribuir al proyecto?
Aunque no estamos buscando contribuciones activas en este momento, valoramos tu feedback. No dudes en compartir tus ideas o sugerencias a través de la sección de 'issues' de nuestro repositorio de GitHub.

### ¿Qué hago si encuentro un error o un problema?
Si encuentras un error o tienes algún problema con el proyecto, por favor, repórtalo en la sección de 'issues' de nuestro repositorio de GitHub.

---

*Este documento se actualizará regularmente para reflejar los cambios más recientes en el proyecto y responder a las preguntas de la comunidad.*
