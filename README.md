# AnalizadorDeProyecto

## Descripción
El `AnalizadorDeProyecto` es una herramienta poderosa diseñada para ayudar a los desarrolladores a analizar y mejorar la estructura de sus proyectos de software. Con funcionalidades como la instalación automática de dependencias, análisis avanzado de archivos, y generación de informes detallados, esta herramienta facilita la gestión del código y mejora la eficiencia del desarrollo.

- Compatible con Python 3.9
- Instalación y configuración sencillas
- Análisis detallado con reportes visuales

Empieza rápidamente con nuestra [Guía de Inicio Rápido](https://github.com/AgustinMadygraf/AnalizadorDeProyecto/blob/main/docs/QUICKSTART.MD).

## Arquitectura Limpia y Estructura del Proyecto

El proyecto sigue los principios de Clean Architecture, separando responsabilidades en capas bien definidas para maximizar la mantenibilidad y escalabilidad.

**Estructura principal:**

```
src/
  common/           # Utilidades transversales puras
  domain/           # Lógica de negocio
  application/      # Casos de uso y orquestación
  infrastructure/   # Adaptadores y utilidades técnicas
    file_adapters/  # Manejadores concretos de archivos
  interfaces/       # Puertos (interfaces) para comunicación entre capas
  presentation/     # Lógica de presentación (CLI, UI)
```

- Las utilidades puras se encuentran en `src/common/`.
- Los manejadores de archivos y utilidades técnicas están en `src/infrastructure/`.
- Las interfaces y puertos están en `src/interfaces/`.

---

## Inyección de dependencias y puertos

La inyección de dependencias se realiza en `src/presentation/cli_entry.py`, donde se instancian los adaptadores concretos y se pasan a los orquestadores como puertos (interfaces). Esto permite desacoplar la lógica de negocio de los detalles de infraestructura y facilita el testeo y la extensión del sistema.

---

## Versión de Python
El `AnalizadorDeProyecto` ha sido actualizado para ser compatible y ha sido testeado con Python 3.9, asegurando una mayor eficiencia y compatibilidad con las versiones más recientes. *Nota: Se recomienda verificar periódicamente las actualizaciones de Python y las dependencias para mantener la compatibilidad y seguridad.*

## Configuración del Entorno de Desarrollo

Para configurar el entorno de desarrollo y asegurar que todas las dependencias estén correctamente instaladas, siga los siguientes pasos:

### Crear un Entorno Virtual

1. Abra una terminal en el directorio raíz del proyecto.
2. Ejecute el siguiente comando para crear un entorno virtual:
   ```bash
   python -m venv venv
   ```
   Esto creará un nuevo directorio `venv` en el directorio del proyecto, el cual contendrá el entorno virtual.

### Activar el Entorno Virtual

- En Windows, ejecute:
  ```bash
  .\venv\Scripts\activate
  ```
- En macOS y Linux, ejecute:
  ```bash
  source venv/bin/activate
  ```
  Al activar el entorno virtual, cualquier instalación de paquetes de Python se realizará dentro de este entorno, aislando así las dependencias del proyecto.

### Instalar las Dependencias

Con el entorno virtual activado, instale las dependencias del proyecto ejecutando:
```bash
pip install -r requirements.txt
```
Esto leerá el archivo `requirements.txt` en el directorio raíz del proyecto e instalará las dependencias especificadas.

### Ejecutar el Proyecto

Con el entorno configurado y las dependencias instaladas, ahora puede ejecutar el proyecto utilizando:
```bash
python src/main.py
```

## Uso por Línea de Comandos (CLI)

A partir de la versión 2025.06, el AnalizadorDeProyecto soporta ejecución tanto interactiva como batch/no interactiva.

### Ejecución Interactiva (menú clásico)
```bash
python run.py
```

### Ejecución Batch (no interactiva)
```bash
python run.py --input <ruta_proyecto> [--output <archivo_salida>] [--modo resumen|completo] [--incluir-todo] --no-interactive
```

> También puedes usar `--input -` para leer desde stdin (útil para pipes o redirección):
> ```bash
> cat archivo.txt | python run.py --input - --no-interactive
> ```
> En modo batch, todos los argumentos requeridos deben ser provistos por flags. Si falta `--input`, el programa mostrará un error y finalizará con código 1. No se solicitará ningún dato por pantalla.

#### Ejemplo:
```bash
python run.py --input ./mi_proyecto --output reporte.txt --modo completo --incluir-todo --no-interactive
```

### Flags disponibles
- `--input`, `-i` : Ruta del directorio o archivo a analizar (obligatorio en modo batch)
- `--output`, `-o` : Ruta del archivo de salida (opcional)
- `--modo`, `-m` : Modo de análisis (`resumen` o `completo`)
- `--incluir-todo` : Incluir el archivo `todo.txt` en el análisis
- `--no-interactive` : Ejecutar en modo batch/no interactivo
- `--help`, `-h` : Mostrar ayuda y salir

> Si no se especifica `--no-interactive`, el programa inicia en modo menú clásico.

## Ejemplos Avanzados de Uso

### Análisis batch leyendo desde stdin
```bash
cat archivo.txt | python run.py --input - --no-interactive
```

### Análisis batch con salida a archivo
```bash
python run.py --input ./proyecto --output reporte.txt --modo completo --incluir-todo --no-interactive
```

### Análisis sin colores (accesibilidad o redirección)
```bash
python run.py --input ./proyecto --no-interactive --no-color > salida.txt
```

### Verificar código de salida tras error
```bash
python run.py --input ./noexiste --no-interactive || echo "Error: %ERRORLEVEL%"
```

## Errores Comunes y Mensajes

- **[ERROR] Falta argumento obligatorio**
  - Mensaje: `[ERROR] Falta el argumento --input. Sugerencia: use --help para ver los flags requeridos.`
  - Código de salida: 1

- **[ERROR] Ruta no encontrada o inaccesible**
  - Mensaje: `[ERROR] La ruta proporcionada no es válida o no se puede acceder a ella.`
  - Sugerencia: `Verifique que la ruta exista, tenga permisos de lectura y sea un directorio válido.`
  - Código de salida: 1

- **[ERROR] Error interno inesperado**
  - Mensaje: `[ERROR] Ha ocurrido un error inesperado. Por favor, reporte este problema.`
  - Código de salida: 3

- **[INFO] Ejecución interrumpida por el usuario**
  - Mensaje: `[INFO] Ejecución interrumpida por el usuario.`
  - Código de salida: 130

- **[INFO] Uso de idioma no soportado**
  - Mensaje: `[WARN] No se pudo cargar el archivo de idioma 'fr': ... Usando español por defecto.`
  - Código de salida: 0 (continúa con fallback)

## Troubleshooting (Solución de Problemas)

- Si recibes un error de argumentos, revisa los flags requeridos con `--help` o `--help-modo`.
- Si el idioma no cambia, verifica la variable de entorno `ANALIZADOR_LANG` o el flag `--lang`.
- Si la salida tiene caracteres extraños, usa `--no-color` o redirige la salida a un archivo.
- Para ayuda sobre modos o submenús, usa `--help-modo` o `--help-optimizacion`.

## Manteniendo tu repositorio limpio

Es vital para la integridad y seguridad de tu código mantener ciertos archivos y directorios fuera del control de versiones. Por ello, te recordamos incluir el directorio `.pytest_cache/` en tu archivo `.gitignore`. Esto evitará la subida accidental de datos de prueba y configuraciones específicas de tu entorno de desarrollo al repositorio.

```plaintext
# Ejemplo de contenido para .gitignore
.pytest_cache/
.env
*.log
```

Asegurarte de que tu `.gitignore` esté correctamente configurado puede ahorrarte problemas de seguridad y mantenimiento a largo plazo.

## Guía de Contribución

1. Forkea el repositorio y crea una rama descriptiva.
2. Sigue la estructura de carpetas y convenciones del proyecto.
3. Agrega o actualiza tests si modificas lógica de negocio.
4. Documenta tus cambios en el README o en la sección correspondiente.
5. Abre un Pull Request detallando el propósito y el impacto de tu contribución.

Para dudas o sugerencias, utiliza la sección de 'issues' en GitHub.

## Preguntas Frecuentes (FAQ)

### ¿Cómo puedo empezar a usar el AnalizadorDeProyecto?

Dependiendo del método de instalación elegido, asegúrate de que el entorno virtual esté activo (`pipenv shell` para pipenv o activar el entorno virtual estándar) y luego ejecuta `src/main.py` en la raíz de tu proyecto para comenzar el análisis.

### ¿En qué sistemas operativos funciona el AnalizadorDeProyecto?

El proyecto se ha actualizado para asegurar la compatibilidad con sistemas operativos que soporten Python 3.9, mejorando así nuestra cobertura en distintas plataformas.

### ¿Puedo contribuir al proyecto?

Aunque no estamos buscando contribuciones activas en este momento, valoramos tu feedback. No dudes en compartir tus ideas o sugerencias a través de la sección de 'issues' de nuestro repositorio de GitHub.

### ¿Qué hago si encuentro un error o un problema?

Si encuentras un error o tienes algún problema con el proyecto, por favor, repórtalo en la sección de 'issues' de nuestro repositorio de GitHub.

### ¿Puedo extender el AnalizadorDeProyecto con plugins o extensiones?

Actualmente no se soportan plugins/extensiones. Esta funcionalidad se evaluará en el futuro según la demanda y la estabilidad del core. Si tienes un caso de uso concreto, abre un issue para discutirlo.

## ¿Quieres ayudarnos a mejorar?

Por favor, utiliza la [plantilla de feedback](FEEDBACK.md) para reportar tu experiencia, errores o sugerencias.

## Cambios recientes (junio 2025)

- Se implementó modo batch/no interactivo (`--no-interactive`) con códigos de salida estándar.
- Se robusteció el manejo de errores y mensajes en modo interactivo (máx. 3 intentos para rutas inválidas).
- Todos los errores relevantes retornan códigos de salida Unix (`0` éxito, `1` error usuario, `2` error sistema, `3` error inesperado, `130` interrupción).
- La ayuda (`--help`) y los ejemplos de uso fueron revisados y ampliados.

## Validación recomendada

1. **Modo batch**:
   - Ejecutar: `python run.py --input ./noexiste --no-interactive` → Debe mostrar error y código de salida 1.
   - Ejecutar: `python run.py --input ./proyecto --no-interactive` → Debe finalizar con éxito (código 0) si la ruta es válida.
2. **Modo interactivo**:
   - Ingresar rutas inválidas 3 veces seguidas → Debe abortar con mensaje claro.
   - Interrumpir con Ctrl+C → Debe mostrar mensaje y salir con código 130.
3. **Ayuda y ejemplos**:
   - Ejecutar: `python run.py --help` → Debe mostrar flags y ejemplos claros.

## Soporte de idioma (internacionalización)

- Puedes elegir idioma español o inglés con el flag `--lang` o la variable de entorno `ANALIZADOR_LANG`.
- Ejemplo:
  ```bash
  python run.py --lang en --no-interactive --input ./project
  ANALIZADOR_LANG=en python run.py --no-interactive --input ./project
  ```
- Los mensajes principales y errores se mostrarán en el idioma seleccionado.

## Internacionalización: pluralización y fallback

- El sistema de mensajes soporta español e inglés mediante archivos JSON.
- Si se solicita un idioma no soportado, se muestra advertencia y se usa español por defecto.
- Si falta una clave de mensaje, se muestra el texto interno por defecto (fallback).
- Actualmente, la pluralización es básica: los mensajes pueden diferenciar singular/plural solo si se define en los archivos de idioma.
- Para mejorar la pluralización, puedes proponer una estructura tipo `{clave}_plural` en los archivos JSON y lógica condicional en el código.

## Accesibilidad y TTY

- Si la salida no es TTY o usas `--no-color`, los colores se desactivan automáticamente.
- Los mensajes principales son texto plano, compatibles con lectores de pantalla.

## Accesibilidad

- Usa el flag `--no-color` para desactivar colores y mejorar la compatibilidad con lectores de pantalla.
- Puedes redirigir la salida a un archivo y abrirlo con un lector accesible.
- El menú y los mensajes están diseñados para ser claros en texto plano.
- Si tienes sugerencias de mejora en accesibilidad, abre un issue o pull request.

## Backlog de mejoras futuras (priorizado)

1. **Internacionalización** (`--lang` o variable de entorno)
   - Permitir mensajes y ayuda en inglés/español.
   - Beneficio: medio | Esfuerzo: medio
2. **Accesibilidad avanzada**
   - Mejorar compatibilidad con lectores de pantalla y prompts alternativos.
   - Beneficio: medio | Esfuerzo: bajo
3. **Refactor de input y validaciones**
   - Unificar lógica de validación y mensajes de error.
   - Beneficio: medio | Esfuerzo: bajo
4. **Soporte para configuración por archivo (`.analizadorrc`)**
   - Permitir flags y rutas por archivo de configuración.
   - Beneficio: bajo | Esfuerzo: medio
5. **Mejorar tests de integración CLI**
   - Cobertura de casos de error y edge cases.
   - Beneficio: medio | Esfuerzo: bajo
6. **Soporte para plugins/extensiones**
   - Permitir análisis personalizados por el usuario.
   - Beneficio: bajo | Esfuerzo: alto

> **Nota:** Por el momento, la arquitectura de plugins/extensiones no será implementada hasta consolidar la base y recibir feedback real. Si tienes necesidades específicas, por favor abre un issue para discutirlas.

## Demos Visuales (asciinema/GIF)

> ¡Contribuye! Puedes grabar y compartir sesiones de ejemplo usando [asciinema](https://asciinema.org/) o herramientas de grabación de GIFs.
>
> - Para grabar una demo interactiva:
>   ```bash
>   asciinema rec docs/demo_interactivo.cast
>   # Ejecuta: python run.py
>   # Finaliza con Ctrl+D
>   asciinema upload docs/demo_interactivo.cast
>   ```
> - Para grabar una demo batch:
>   Usa [peek](https://github.com/phw/peek) o similar para capturar un GIF de la terminal.
>
> **Enlaces sugeridos:**
> - [Demo Interactivo (asciinema)](docs/demo_interactivo.cast) *(placeholder)*
> - [Demo Batch (GIF)](docs/demo_batch.gif) *(placeholder)*

¿Quieres aportar una demo? Consulta la sección de contribución.