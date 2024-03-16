
# SYSTEM

## Contexto del Proyecto
Este prompt está diseñado para ser utilizado en conjunto con la estructura de directorios y archivos de un proyecto de software, enfocándose en implementar mejoras en las buenas prácticas de desarrollo de software.

## Objetivo
El objetivo es analizar un proyecto de software para identificar áreas específicas donde aplicar mejores prácticas de programación, diseño UX/UI, y técnicas de machine learning para optimización y automatización. Tendrás que prestar atención al archivo REAMDE.md

# USER

### Pasos para la Mejora del Proyecto
1. **Análisis Automatizado del Proyecto:**
   - Realizar una revisión  de la estructura de directorios y archivos, y contenido del proyecto utilizando pruebas automáticas y análisis de rendimiento.

2. **Identificación de Áreas de Mejora con Machine Learning:**
   - Utilizar algoritmos de machine learning para identificar patrones de errores comunes, optimización de rendimiento y áreas clave para mejoras.

3. **Sugerencias Específicas y Refactorización:**
   - Proporcionar recomendaciones detalladas y automatizadas para las mejoras identificadas, incluyendo sugerencias de refactorización y optimización.

4. **Plan de Acción Detallado con Retroalimentación:**
   - Desarrollar un plan de acción con pasos específicos, incluyendo herramientas y prácticas recomendadas.
   - Implementar un sistema de retroalimentación para ajustar continuamente el proceso de mejora basándose en el uso y rendimiento.

5. **Implementación y Evaluación Continua:**
   - Indicar archivos o componentes específicos para mejoras.
   - Evaluar el impacto de las mejoras y realizar ajustes basándose en retroalimentación continua.

### Consideraciones para la Mejora
- **Desarrollo de Software:**
   - Examinar estructura de archivos, logging, código duplicado, ciberseguridad, nomenclatura y prácticas de codificación.
   - Incorporar pruebas automáticas y análisis de rendimiento.

- **Tecnologías Utilizadas:**
   - El proyecto utiliza Python, PHP, HTML, MySQL y CSS. Las recomendaciones serán compatibles con estas tecnologías.

- **Documentación y Conocimiento Compartido:**
   - Mantener una documentación detallada de todos los cambios y mejoras para facilitar el aprendizaje y la mejora continua.



## Estructura de Carpetas y Archivos
```bash
AnalizadorDeProyecto/
    installer.py
    README.md
    requirements.txt
    config/
        path.txt
        prompt_aprender.md
        prompt_error.md
        prompt_upd_0.md
        prompt_upd_1.md
        prompt_upd_2.md
        prompt_upd_3.md
        recomendaciones.md
    DOCS/
        00-Prompt-for-ProjectAnalysis.md
        02-diagrama_flujo.txt
        CONTRIBUTING.md
        QUICKSTART.MD
    src/
        GestArch.py
        InterfazHM.py
        ManiArch.py
        Principal.py
        SalidDatos.py
        UtilSist.py
        config/
        logs/
            config_logger.py
            __pycache__/
        __pycache__/
    __pycache__/
```


## Contenido de Archivos Seleccionados

### C:\AppServ\www\AnalizadorDeProyecto\installer.py
```plaintext
#installer.py
import subprocess
import os
import sys
from src.logs.config\_logger import configurar\_logging
import winshell
from win32com.client import Dispatch

# Configuración del logger
logger = configurar\_logging\(\)

def crear\_acceso\_directo\(ruta\_archivo\_bat, directorio\_script\):
    escritorio = winshell.desktop\(\)
    ruta\_acceso\_directo = os.path.join\(escritorio, "AnalizadorDeProyecto.lnk"\)
    ruta\_icono = os.path.join\(directorio\_script, "config", "AnalizadorDeProyecto.ico"\)

    if not os.path.isfile\(ruta\_icono\):
        logger.error\(f"El archivo de icono '{ruta\_icono}' no existe."\)
        return False

    try:
        shell = Dispatch\('WScript.Shell'\)
        acceso\_directo = shell.CreateShortCut\(ruta\_acceso\_directo\)
        acceso\_directo.Targetpath = ruta\_archivo\_bat
        acceso\_directo.WorkingDirectory = directorio\_script
        acceso\_directo.IconLocation = ruta\_icono  
        acceso\_directo.save\(\)
        logger.info\(f"Acceso directo {'actualizado' if os.path.isfile\(ruta\_acceso\_directo\) else 'creado'} exitosamente."\)
        return True
    except Exception as e:
        logger.error\(f"Error al crear/actualizar el acceso directo: {e}", exc\_info=True\)
        return False

def main\(\):
    directorio\_script = os.path.dirname\(os.path.abspath\(\_\_file\_\_\)\)
    limpieza\_pantalla\(\)
    logger.info\("Iniciando instalador"\)

    #instalar\_dependencias\(directorio\_script\)
    ruta\_archivo\_bat = os.path.join\(directorio\_script, 'AnalizadorDeProyecto.bat'\)
    if not os.path.isfile\(ruta\_archivo\_bat\):
        logger.info\("Creando archivo 'AnalizadorDeProyecto.bat'"\)
        crear\_archivo\_bat\(directorio\_script, sys.executable\)
    
    crear\_acceso\_directo\(ruta\_archivo\_bat, directorio\_script\)

def instalar\_dependencias\(directorio\_script\):
    ruta\_requirements = os.path.join\(directorio\_script, 'requirements.txt'\)
    if os.path.isfile\(ruta\_requirements\):
        with open\(ruta\_requirements\) as file:
            for package in \[line.strip\(\) for line in file if line.strip\(\) and not line.startswith\('#'\)\]:
                try:
                    subprocess.run\(\[sys.executable, "-m", "pip", "install",

 package\], capture\_output=True, text=True, check=True\)
                    logger.info\(f"Instalado o actualizado: {package}"\)
                except subprocess.CalledProcessError as e:
                    logger.error\(f"Error al instalar la dependencia {package}: {e.output}"\)
        logger.info\("Verificación y actualización de dependencias completada."\)
    else:
        logger.warning\("Archivo 'requirements.txt' no encontrado. No se instalaron dependencias adicionales."\)

def crear\_archivo\_bat\(directorio\_script, python\_executable\):
    ruta\_main\_py = os.path.join\(directorio\_script, 'src', 'Principal.py'\)
    ruta\_archivo\_bat = os.path.join\(directorio\_script, 'AnalizadorDeProyecto.bat'\)

    contenido\_bat = \(
        "@echo off\n"
        "setlocal\n"
        "\n"
        "set \"SCRIPT\_DIR=%~dp0\"\n"
        "\n"
        "cd /d \"%SCRIPT\_DIR%\"\n"
        "\"{}\" \"{}\"\n".format\(python\_executable, ruta\_main\_py\) +
        "pause\n"
        "endlocal\n"
    \)

    with open\(ruta\_archivo\_bat, 'w'\) as archivo\_bat:
        archivo\_bat.write\(contenido\_bat\)
    logger.info\("Archivo 'AnalizadorDeProyecto.bat' creado exitosamente."\)

def limpieza\_pantalla\(\):
    try:
        os.system\('cls' if os.name == 'nt' else 'clear'\)
        logger.info\("Pantalla limpiada."\)
    except Exception as e:
        logger.error\(f"Error al limpiar la pantalla: {e}"\)

if \_\_name\_\_ == "\_\_main\_\_":
    main\(\)

```

### C:\AppServ\www\AnalizadorDeProyecto\README.md
```plaintext
# AnalizadorDeProyecto

## Descripción
El \`AnalizadorDeProyecto\` es una herramienta avanzada en Python, diseñada para analizar, documentar y mejorar la estructura de proyectos de software. Ideal para la gestión y mantenimiento del código, esta herramienta ofrece funciones mejoradas de verificación, instalación de dependencias, enumeración avanzada de archivos por extensión y generación de informes detallados sobre la arquitectura del proyecto con capacidades de visualización.

## Versión de Python
El \`AnalizadorDeProyecto\` es ahora compatible y ha sido testeado en Python 3.12.2, asegurando una mayor eficiencia y compatibilidad con las últimas versiones. \*Nota: Se recomienda verificar periódicamente las actualizaciones de Python y las dependencias para mantener la compatibilidad y seguridad.\*

## Instalación
Para una experiencia óptima con \`AnalizadorDeProyecto\`, sigue estos comandos en tu terminal para una instalación rápida y fácil:

\`\`\`bash
pip install pyperclip datetime importlib-metadata
\`\`\`

\*\*Nota:\*\* \`importlib-metadata\` sigue siendo esencial para versiones de Python inferiores a 3.8. En versiones 3.8 o superiores, esta librería forma parte del conjunto estándar.

## Uso
Para utilizar \`AnalizadorDeProyecto\` de manera efectiva:
1. Navega a la carpeta raíz de tu proyecto y ejecuta \`AnalizadorDeProyecto.py\`.
2. Cuando se solicite, proporciona la ruta de la carpeta a analizar.
3. Disfruta de las siguientes funcionalidades mejoradas:
   - Enumeración inteligente de archivos en la ruta proporcionada, clasificados por extensión.
   - Generación de informes exhaustivos sobre la estructura del proyecto en formato de texto y visualizaciones gráficas.

\`AnalizadorDeProyecto\` es más que una herramienta; es tu compañero esencial para comprender y mejorar tus proyectos de software.

---

\*\*Actualizaciones Recientes:\*\*
- Mayor compatibilidad con las versiones más recientes de Python.
- Funcionalidades

mejoradas para análisis de estructura de proyectos.
- Nueva capacidad de visualización gráfica para una mejor comprensión de la estructura del proyecto.

\*\*Advertencia:\*\* Asegúrate de tener Python 3.6 o una versión más reciente instalada en tu sistema antes de ejecutar \`AnalizadorDeProyecto\`.

## Preguntas Frecuentes \(FAQ\)

### ¿Cómo puedo empezar a usar el AnalizadorDeProyecto?
Para comenzar, ejecuta \`AnalizadorDeProyecto.py\` en la raíz de tu proyecto. Proporciona la ruta del directorio a analizar cuando se te solicite.

### ¿En qué sistemas operativos funciona el AnalizadorDeProyecto?
Actualmente, se ha probado en sistemas Windows con Python 3.15.2. Se planea probar y asegurar la compatibilidad con Ubuntu Mate en un futuro cercano.

### ¿Puedo contribuir al proyecto?
Aunque no estamos buscando contribuciones activas en este momento, cualquier feedback es siempre bienvenido. No dudes en compartir tus ideas o sugerencias.

### ¿Qué hago si encuentro un error o un problema?
Por favor, reporta cualquier error o problema en la sección de 'issues' de nuestro repositorio de GitHub.

---

\*Este documento se actualizará regularmente para reflejar los cambios más recientes en el proyecto y responder a las preguntas de la comunidad.\*


```

### C:\AppServ\www\AnalizadorDeProyecto\requirements.txt
```plaintext
aiofiles==23.2.1
altgraph==0.17.4
annotated-types==0.6.0
anyio==4.1.0
certifi==2023.11.17
charset-normalizer==3.3.2
chatterbot-corpus==1.2.0
click==7.1.2
click-didyoumean==0.3.0
colorama==0.4.6
DateTime==5.4
distro==1.8.0
filelock==3.13.1
fsspec==2023.12.2
gpt4all==2.0.2
h11==0.14.0
httpcore==1.0.2
httpx==0.25.2
huggingface-hub==0.20.2
idna==3.6
importlib==1.0.4
importlib-metadata==7.0.1
openai==1.3.8
packaging==23.2
pefile==2023.2.7
pydantic==2.5.2
pydantic\_core==2.14.5
pyinstaller==6.3.0
pyinstaller-hooks-contrib==2023.12
pyperclip==1.8.2
python-dotenv==1.0.0
python-telegram-bot==20.7
pytz==2023.3.post1
pywin32==306
pywin32-ctypes==0.2.2
PyYAML==6.0.1
requests==2.31.0
setuptools==69.0.2
sniffio==1.3.0
telegram==0.0.1
tqdm==4.66.1
typing\_extensions==4.9.0
urllib3==2.1.0
wheel==0.41.3
winshell==0.6
zipp==3.17.0
zope.interface==6.1

```

### C:\AppServ\www\AnalizadorDeProyecto\config\path.txt
```plaintext
C:\AppServ\www\AnalizadorDeProyecto
```

### C:\AppServ\www\AnalizadorDeProyecto\config\prompt_aprender.md
```plaintext


# SYSTEM

## Contexto del Prompt
Este prompt está diseñado para facilitar el proceso de enseñanza y aprendizaje del software \[INSERTAR\_NOMBRE\_PROYECTO\] que se encuentra a continuación.

## Objetivo del Prompt
El objetivo es guiar al usuario a través de un entendimiento profundo del software, abarcando aspectos tales como su arquitectura, funcionalidades clave, uso efectivo y mejores prácticas de desarrollo integradas en el proyecto.

# USER

### Pasos para el Aprendizaje Asistido
1. \*\*Introducción al Proyecto:\*\*
   - Comenzar con una descripción general del software, incluyendo su propósito, características principales y tecnologías utilizadas.

2. \*\*Exploración de la Estructura:\*\*
   - Navegar por la estructura de directorios y archivos del proyecto, explicando la función y relevancia de cada componente.

3. \*\*Análisis Detallado del Código:\*\*
   - Examinar archivos de código seleccionados, discutiendo aspectos clave como lógica de programación, patrones de diseño y comentarios significativos.

4. \*\*Ejecución y Uso del Software:\*\*
   - Guiar en la ejecución del software, mostrando ejemplos prácticos de su uso y funcionamiento.

5. \*\*Prácticas de Desarrollo Integradas:\*\*
   - Destacar las prácticas de desarrollo implementadas en el proyecto, incluyendo estilo de codificación, pruebas y gestión de versiones.

6. \*\*Resolución de Problemas Comunes:\*\*
   - Presentar y resolver problemas comunes o errores típicos que pueden surgir al trabajar con el software.

### Recomendaciones Finales
- \*\*Experimentación Activa:\*\*
   - Animar al usuario a experimentar activamente con el código, haciendo modificaciones y observando los resultados.
- \*\*Consultas Adicionales:\*\*
   - Fomentar la formulación de preguntas específicas al LLM para aclarar dudas o profundizar en temas particulares.

```

### C:\AppServ\www\AnalizadorDeProyecto\config\prompt_error.md
```plaintext
# SYSTEM

## Contexto del Prompt
Este prompt está diseñado para asistir en la identificación y resolución de errores en un proyecto de software. El objetivo es guiar a un agente de IA experto en programación para analizar y proponer soluciones efectivas a los problemas encontrados.

# USER

### Pasos para la Detección y Solución de Errores
1. \*\*Análisis Exhaustivo del Proyecto:\*\*
   - Revisar detalladamente la estructura del proyecto, incluyendo el código y la documentación, para comprender el contexto y el flujo de trabajo actual.

2. \*\*Identificación de Errores:\*\*
   - Investigar y localizar áreas del proyecto donde se sospecha que hay errores. Estos pueden incluir errores de sintaxis, lógica, rendimiento, seguridad o diseño.
   - Utilizar herramientas de depuración y análisis de código, si están disponibles, para facilitar la identificación de problemas.

3. \*\*Propuesta de Soluciones:\*\*
   - Una vez identificado el error, proporcionar una solución específica y justificada. Esta solución debe estar basada en las mejores prácticas de programación y en la naturaleza del error detectado.

4. \*\*Plan de Acción Detallado:\*\*
   - Desarrollar un plan de acción paso a paso para implementar la solución propuesta. Este plan debe incluir recomendaciones sobre cambios de código, ajustes de configuración o cualquier otra acción necesaria.

5. \*\*Implementación y Pruebas:\*\*
   - Guiar en la implementación de la solución y sugerir pruebas para validar su efectividad.
   - Recomendar pruebas unitarias, de integración o funcionales, según corresponda, para asegurar que el error se haya solucionado completamente sin introducir nuevos problemas.

### Enfoque General
- Mantener un enfoque sistemático y metódico para asegurar que todos los aspectos del error sean considerados.
- Priorizar la claridad y la eficiencia en las soluciones propuestas.


```

### C:\AppServ\www\AnalizadorDeProyecto\config\prompt_upd_0.md
```plaintext

# SYSTEM

## Contexto del Proyecto
Este prompt está diseñado para ser utilizado en conjunto con la estructura de directorios y archivos de un proyecto de software, enfocándose en implementar mejoras en las buenas prácticas de desarrollo de software.

## Objetivo
El objetivo es analizar un proyecto de software para identificar áreas específicas donde aplicar mejores prácticas de programación, diseño UX/UI, y técnicas de machine learning para optimización y automatización. Tendrás que prestar atención al archivo REAMDE.md

# USER

### Pasos para la Mejora del Proyecto
1. \*\*Análisis Automatizado del Proyecto:\*\*
   - Realizar una revisión  de la estructura de directorios y archivos, y contenido del proyecto utilizando pruebas automáticas y análisis de rendimiento.

2. \*\*Identificación de Áreas de Mejora con Machine Learning:\*\*
   - Utilizar algoritmos de machine learning para identificar patrones de errores comunes, optimización de rendimiento y áreas clave para mejoras.

3. \*\*Sugerencias Específicas y Refactorización:\*\*
   - Proporcionar recomendaciones detalladas y automatizadas para las mejoras identificadas, incluyendo sugerencias de refactorización y optimización.

4. \*\*Plan de Acción Detallado con Retroalimentación:\*\*
   - Desarrollar un plan de acción con pasos específicos, incluyendo herramientas y prácticas recomendadas.
   - Implementar un sistema de retroalimentación para ajustar continuamente el proceso de mejora basándose en el uso y rendimiento.

5. \*\*Implementación y Evaluación Continua:\*\*
   - Indicar archivos o componentes específicos para mejoras.
   - Evaluar el impacto de las mejoras y realizar ajustes basándose en retroalimentación continua.

### Consideraciones para la Mejora
- \*\*Desarrollo de Software:\*\*
   - Examinar estructura de archivos, logging, código duplicado, ciberseguridad, nomenclatura y prácticas de codificación.
   - Incorporar pruebas automáticas y análisis de rendimiento.

- \*\*Tecnologías Utilizadas:\*\*
   - El proyecto utiliza Python, PHP, HTML, MySQL y CSS. Las recomendaciones serán compatibles con estas tecnologías.

- \*\*Documentación y Conocimiento Compartido:\*\*
   - Mantener una documentación detallada de todos los cambios y mejoras para facilitar el aprendizaje y la mejora continua.


```

### C:\AppServ\www\AnalizadorDeProyecto\config\prompt_upd_1.md
```plaintext
https://flowchart.fun/#


Comienza a escribir
  Considere: Agregar una etiqueta
    Sí: Opción A
      Usa un ID para conectar #connect
    No: Opción B
      \(#connect\)
        ¡Ahora borra el texto y pruebalo tú mismo\!


Etiqueta de nodo
El texto en una línea crea un nodo con el texto como etiqueta

ID de nodo, clases, atributos
ID
Valor de texto único para identificar un nodo

Clases
Usar clases para agrupar nodos

Atributos
Almacenar cualquier dato asociado a un nodo

Bordes
Crear un borde entre dos nodos se realiza al sangrar el segundo nodo debajo del primero

Etiqueta de borde
El texto seguido de dos puntos y un espacio crea un borde con el texto como etiqueta

ID de borde, Clases, Atributos
Los bordes también pueden tener ID, clases y atributos antes de la etiqueta

Referencias
Las referencias se utilizan para crear bordes entre los nodos creados en otro lugar del documento

Referencia por etiqueta
Referenciando un nodo por su etiqueta exacta

Referencia por ID
Referenciando un nodo por su ID único

Referencia por clase
Referenciando múltiples nodos con la misma clase asignada

Contenedores
Los contenedores son nodos que contienen otros nodos. Se declaran usando llaves.

Clases de Estilo
La mejor manera de cambiar los estilos es hacer clic derecho en un nodo o un borde y seleccionar el estilo deseado.

Colores de nodo
Los colores incluyen rojo, naranja, amarillo, azul, morado, negro, blanco y gris.

Formas de nodo
Las formas posibles son: rectangle, roundrectangle, ellipse, triangle, pentagon, hexagon, heptagon, octagon, star, barrel, diamond, vee, rhomboid, right-rhomboid, polygon, tag, round-rectangle, cut-rectangle, bottom-round-rectangle, and concave-hexagon
```

### C:\AppServ\www\AnalizadorDeProyecto\config\prompt_upd_2.md
```plaintext

# SYSTEM

## Contexto del Proyecto
Este prompt se utiliza para generar automáticamente un archivo TODO.txt en formato Markdown. Está diseñado para proyectos de software, con énfasis en la programación, diseño UX/UI y machine learning.

## Objetivo
El objetivo es proporcionar un TODO.txt, resaltando áreas específicas para aplicar mejores prácticas de programación, diseño UX/UI y técnicas de machine learning. Se enfoca en optimización y automatización, basándose en el análisis del proyecto de software. La respuesta debe omitir descripción del análisis ya que debe limitarse al archivo TXT dentro de "\`\`\`" 

# USER

/start

### Contenido del TODO.txt
El archivo TODO.txt debe incluir tareas pendientes específicas para la mejora del proyecto, estructuradas de la siguiente manera en formato Markdown:
\`\`\`
# To Do List

## \[nombre\_del\_archivo\]
- Situación: \[Pendiente/En\_Proceso/Finalizado\]
- Análisis del Ingeniero de Software: \[Detalle\_de\_la\_mejora\_específica\_propuesta\_a\_partir\_del\_análisis\_realizado\]

## \[nombre\_del\_archivo2\]
- Situación: \[Pendiente/En\_Proceso/Finalizado\]
- Análisis del Ingeniero de Software: \[Detalle\_de\_la\_mejora\_específica\_propuesta\_a\_partir\_del\_análisis\_realizado\]

\`\`\`
\(Continuar con más archivos y tareas según sea necesario\)

```

### C:\AppServ\www\AnalizadorDeProyecto\config\prompt_upd_3.md
```plaintext
Proporcioname código modificado para implementar la siguiente mejora entre triple comillas 
"""
\[viene\_desde\_TODO.txt\]
"""

Código a mejorar:
"""
\[contenido\_filename\]
"""
```

### C:\AppServ\www\AnalizadorDeProyecto\config\recomendaciones.md
```plaintext


# Guía de Recomendaciones para el Desarrollo de Software

## Introducción
Esta guía ofrece recomendaciones esenciales para el desarrollo eficiente y efectivo de software, asegurando la calidad, mantenibilidad y escalabilidad del código.

## Mejores Prácticas

### Diseño y Arquitectura
1. \*\*Principios SOLID:\*\* Sigue los principios SOLID para un diseño orientado a objetos limpio y mantenible.
2. \*\*Patrones de Diseño:\*\* Utiliza patrones de diseño establecidos para resolver problemas comunes de manera eficiente.

### Estilo de Codificación
1. \*\*Consistencia:\*\* Mantén un estilo de codificación consistente en todo el proyecto.
2. \*\*Nomenclatura Clara:\*\* Usa nombres descriptivos para variables, funciones y clases.
3. \*\*Comentarios y Documentación:\*\* Documenta el código donde sea necesario, especialmente en bloques de código complejos.

### Pruebas
1. \*\*Pruebas Unitarias:\*\* Escribe pruebas unitarias para validar cada componente de manera aislada.
2. \*\*Pruebas de Integración:\*\* Asegúrate de que los componentes del sistema funcionen juntos correctamente.
3. \*\*Automatización de Pruebas:\*\* Utiliza herramientas para automatizar las pruebas y asegurar la calidad continua.

### Control de Versiones
1. \*\*Uso de Git:\*\* Utiliza sistemas de control de versiones como Git para rastrear y gestionar cambios en el código.
2. \*\*Commits Claros:\*\* Escribe mensajes de commit claros y descriptivos.
3. \*\*Revisión de Código:\*\* Practica revisiones de código regulares para mejorar la calidad y fomentar la colaboración.

### Seguridad y Rendimiento
1. \*\*Codificación Segura:\*\* Sigue las prácticas recomendadas de seguridad para prevenir vulnerabilidades.
2. \*\*Optimización:\*\* Optimiza el código para mejorar el rendimiento, especialmente en áreas críticas.

## Herramientas y Tecnologías
1. \*\*IDEs y Editores de Código:\*\* Utiliza herramientas que mejoren la productividad, como IDEs con funciones de depuración y resaltado de sintaxis.
2. \*\*Frameworks y Bibliotecas:\*\* Mantente al día con frameworks y bibliotecas relevantes para tu stack tecnológico.

## Mantenimiento y Escalabilidad
1. \*\*Código Mantenible:\*\* Escribe código pensando en la facilidad de mantenimiento y futuras modificaciones.
2. \*\*Escalabilidad:\*\* Diseña sistemas pensando en la escalabilidad desde el principio.

## Conclusión
Siguiendo estas recomendaciones, puedes mejorar significativamente la calidad y eficiencia de tus proyectos de desarrollo de software. Recuerda que el aprendizaje y la adaptación constantes son claves en el campo en constante evolución del desarrollo de software.

```

### C:\AppServ\www\AnalizadorDeProyecto\DOCS\02-diagrama_flujo.txt
```plaintext
https://flowchart.fun/#

Principal.py\nmain\(\)
  Principal.py\ninicializar\(\)
    UtilSist.py\nLimpieza\_pantalla\(\)
      Principal.py\ncontrol\_de\_flujo\(\)
        ¿Desea analizar el directorio por defecto?
          Sí: Principal.py\nobtener\_ruta\_default\(\)
            InterfazHM.py\nMenu\_01 #connect
          No: Principal.py\nguardar\_nueva\_ruta\_default\(\)
            \(#connect\)
              Elige un modo
                1 : Implementar mejoras en la programación
                  Principal.py\nprocesar\_archivos\(\) #connect2
                2 : Solucionar errores
                  \(#connect2\)
                3 : Aprendizaje
                  \(#connect2\)

```

### C:\AppServ\www\AnalizadorDeProyecto\DOCS\CONTRIBUTING.md
```plaintext
# Contribuyendo a AnalizadorDeProyecto

¡Estamos encantados de que estés interesado en contribuir a \`AnalizadorDeProyecto\`\! Este documento proporciona las directrices necesarias para contribuir efectivamente a este proyecto.

## Cómo Contribuir

1. \*\*Fork y Clone\*\*:
   - Realiza un "fork" del proyecto en tu cuenta de GitHub y luego clona tu fork localmente.

2. \*\*Configura tu Entorno de Trabajo\*\*:
   - Asegúrate de tener Python 3.6 o superior instalado.
   - Instala las dependencias necesarias con \`pip install -r requirements.txt\`.

3. \*\*Encuentra una Tarea para Trabajar\*\*:
   - Puedes comenzar buscando en los 'issues' abiertos, especialmente aquellos marcados como "bueno para principiantes" o "ayuda necesitada".

4. \*\*Trabaja en tu Feature o Bugfix\*\*:
   - Crea una nueva rama para cada feature o bugfix.
   - Escribe código limpio y testeable.
   - Asegúrate de seguir las convenciones de codificación del proyecto.

5. \*\*Pruebas\*\*:
   - Añade pruebas para tu nueva funcionalidad o corrección de errores.
   - Ejecuta las pruebas existentes para asegurarte de que no has introducido nuevos errores.

6. \*\*Documentación\*\*:
   - Actualiza la documentación para reflejar cualquier cambio en la funcionalidad o la adición de nuevas características.

7. \*\*Envía un Pull Request\*\*:
   - Haz un "push" de tu rama a tu fork y envía un pull request \(PR\) al repositorio principal.
   - Describe en el PR los cambios que has realizado y cualquier otra información relevante.

8. \*\*Revisión del Código\*\*:
   - Espera a que un mantenedor revise tu PR. Puede que te pidan realizar cambios adicionales para mejorar tu contribución.

## Directrices

- \*\*Código de Conducta\*\*: Mantén una comunicación respetuosa y profesional en todas tus interacciones dentro del proyecto.
- \*\*Estilo de Código\*\*: Adhiérete al estilo de codificación establecido en el proyecto. Si hay una guía de estilo, síguela.

## Preguntas y Ayuda

- Si tienes alguna pregunta o necesitas ayuda, no dudes en abrir un 'issue' solicitando asistencia o dirigiéndote a nuestros canales de comunicación.

¡Gracias por contribuir al \`AnalizadorDeProyecto\`\!

```

### C:\AppServ\www\AnalizadorDeProyecto\src\GestArch.py
```plaintext
#SCR/GestArch.py
import pyperclip
import os
import time
import fnmatch
import re
from logs.config\_logger import configurar\_logging

# Configuración del logger
logger = configurar\_logging\(\)
ruta\_proyecto = "C:\AppServ\www\AnalizadorDeProyecto"

def esta\_en\_gitignore\(ruta\_archivo, ruta\_proyecto\):
    """
    Verifica si un archivo está listado en .gitignore utilizando expresiones regulares para mejorar la eficiencia.

    Args:
        ruta\_archivo \(str\): Ruta del archivo a verificar.
        ruta\_proyecto \(str\): Ruta del directorio del proyecto que contiene .gitignore.

    Returns:
        bool: True si el archivo está en .gitignore, False en caso contrario.
    """
    ruta\_gitignore = os.path.join\(ruta\_proyecto, '.gitignore'\)
    try:
        with open\(ruta\_gitignore, 'r', encoding='utf-8'\) as gitignore:
            gitignore\_content = gitignore.read\(\)
            # Crear una expresión regular basada en cada línea del .gitignore
            for pattern in gitignore\_content.splitlines\(\):
                regex = fnmatch.translate\(pattern.strip\(\)\)
                if re.match\(regex, ruta\_archivo\):
                    return True
    except FileNotFoundError:
        logger.warning\(f"No se encontró el archivo .gitignore en {ruta\_proyecto}"\)
    return False

def leer\_archivo\(nombre\_archivo, extensiones\_permitidas=\['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt'\]\):
    """
    Lee el contenido de un archivo de texto y lo devuelve, excluyendo archivos que pesen más de 10KB.

    Args:
        nombre\_archivo \(str\): Ruta del archivo a leer.
        extensiones\_permitidas \(list\): Lista de extensiones permitidas para leer.

    Returns:
        str: Contenido del archivo, None si el archivo es mayor a 10KB o no cumple con otras condiciones.
    """
    if not isinstance\(nombre\_archivo, str\):
        logger.warning\(f"Tipo de dato incorrecto para nombre\_archivo: {type\(nombre\_archivo\)}. Se esperaba una cadena \(str\)."\)
        return None

    if not any\(nombre\_archivo.endswith\(ext\) for ext in extensiones\_permitidas\):
        logger.warning\(f"Extensión de archivo no permitida para lectura: {nombre\_archivo}"\)
        return None

    if not os.path.isfile\(nombre\_archivo\):
        logger.warning\(f"El nombre del archivo no corresponde a un archivo: {nombre\_archivo}"\)
        return None

    if esta\_en\_gitignore\(nombre\_archivo, ruta\_proyecto\):
        logger.warning\(f"El archivo '{nombre\_archivo}' está listado en .gitignore y no será leído."\)
        return None

    if os.path.getsize\(nombre\_archivo\) > 10240:
        logger.warning\(f"El archivo '{nombre\_archivo}' excede el tamaño máximo permitido de 10KB."\)
        return None

    try:
        with open\(nombre\_archivo, 'r', encoding='utf-8'\) as archivo:
            contenido = archivo.read\(\)
    except \(FileNotFoundError, OSError, UnicodeDecodeError\) as e:
        logger.error\(f"Error al leer el archivo {nombre\_archivo}: {e}"\)
        return None

    if nombre\_archivo.endswith\('.sql'\):
        return procesar\_sql\(contenido\)
    else:
        return contenido

def procesar\_sql\(contenido\_sql\):
    lineas = contenido\_sql.split\('\n'\)
    lineas\_procesadas = \[\]
    dentro\_de\_insert = False
    for linea in lineas:
        if 'INSERT INTO' in linea:
            dentro\_de\_insert = True
            lineas\_procesadas.append\(linea\)  # Añadir la primera línea del INSERT
        elif dentro\_de\_insert and ';' in linea:
            lineas\_procesadas.append\(linea\)  # Añadir la última línea del INSERT
            dentro\_de\_insert = False
        elif dentro\_de\_insert:
            # Opcional: Añadir alguna indicación de que se han omitido líneas
            pass
    return '\n'.join\(lineas\_procesadas\)

def copiar\_contenido\_al\_portapapeles\(nombre\_archivo\_salida\):
    """
    Copia el contenido de un archivo al portapapeles.

    Args:
        nombre\_archivo\_salida \(str\): Ruta del archivo cuyo contenido se copiará.
    """
    contenido = leer\_archivo\(nombre\_archivo\_salida\)
    if contenido is not None:
        try:
            pyperclip.copy\(contenido\)
            logger.info\(f"El contenido del archivo '{nombre\_archivo\_salida}' ha sido copiado al portapapeles."\)
            time.sleep\(1\)
            print\(""\)
        except pyperclip.PyperclipException as e:
            logger.error\(f"No se pudo copiar al portapapeles: {e}"\)

def verificar\_existencia\_archivo\(nombre\_archivo\):
    """
    Verifica si un archivo existe.

    Args:
        nombre\_archivo \(str\): Ruta del archivo a verificar.

    Returns:
        bool: True si el archivo existe, False en caso contrario.
    """
    return os.path.exists\(nombre\_archivo\)

```

### C:\AppServ\www\AnalizadorDeProyecto\src\InterfazHM.py
```plaintext
#SCR/InterfazHM.py
import os
import time
from logs.config\_logger import configurar\_logging
from GestArch import copiar\_contenido\_al\_portapapeles

# Configuración del logger
logger = configurar\_logging\(\)


OPCIONES\_MENU\_1 = {
    1: 'config\prompt\_upd\_0.md',
    2: 'config\prompt\_error.md',
    3: 'config\prompt\_aprender.md'
}

def menu\_0\(\):
    logger.info\("\n\nPor favor, introduzca la ruta de la carpeta: "\)
    return input\(\).strip\(\)

def solicitar\_opcion\(mensaje, opciones\):
    logger.debug\("Inicio de la selección del modo de operación."\)
    while True:
        logger.info\(mensaje\)
        try:
            opcion = int\(input\(\)\)
            if opcion in opciones:
                return opciones\[opcion\]
            else:
                logger.warning\("Opción no válida. Intente de nuevo."\)
        except ValueError:
            logger.warning\("Entrada no válida. Debes ingresar un número."\)

def menu\_1\(\):
    print\(""\)
    mensaje = "Elige un modo \n\n1 - Implementar mejoras en la programación\n2- Solucionar errores\n3- Aprendizaje\n"
    return solicitar\_opcion\(mensaje, OPCIONES\_MENU\_1\)

def menu\_2\(modo\_prompt, ruta\): 
    instrucciones = \[
        "Abra www.chat.openai.com",
        "Abajo en el centro, haga click derecho donde dice 'Message ChatGPT...'",
        "Haga click en 'pegar'",
        "Presione tecla 'Enter'",
        "Espere a que ChatGPT le haga una devolución",
        f"Mientras tanto, vaya a {ruta}/AMIS",
        "Haga doble click en '01-ProjectAnalysis.md'",
        "Copie la devolución de ChatGPT y pegue en '01-ProjectAnalysis.md'",
        "Guarde '01-ProjectAnalysis.md'"
    \]

    if modo\_prompt == 'config\prompt\_upd\_0.md':
        while True:
            print\(""\)
            for instruccion in instrucciones:
                print\(instruccion\)
                input\("Presione Enter para continuar...\n"\)

            menu\_2\_0 = input\("¿Ya pudo realizar el procedimiento sugerido? \(S/N\): "\).upper\(\)
            if menu\_2\_0 == 'S':
                break
            print\("Por favor, intente nuevamente el procedimiento o solicite asistencia."\)

        while True:
            menu\_2\_1 = input\("¿Está conforme con la respuesta de ChatGPT? \(S/N\): "\).upper\(\)
            if menu\_2\_1 == 'S':
                break
            prompt\_menu2 = "Proporcioname las modificaciones necesarias teniendo en cuentas las sugerencias que me haz realizado"
            copiar\_contenido\_al\_portapapeles\(prompt\_menu2\)
            print\(f"\n\nCopiado al portapapeles: {prompt\_menu2} \n\n"\)
            print\("Por favor pegue abajo en el centro, donde dice 'Message ChatGPT...' y luego presione enter"\)
            input\("Presione Enter una vez haya pegado el texto y recibido una respuesta.\n"\)

        
        # Aquí puedes incluir más instrucciones relacionadas con la creación del diagrama de flujo

    else:
        input\("Presione una tecla para salir"\)
def menu\_3\(modo\_prompt, ruta\):

    instrucciones = \[
        f"Vaya a {ruta}\AMIS\\02-diagrama\_flujo.txt",
        "Seleccione el contenido, copie",
        "Abra el navegador",
        "ingresa a https://flowchart.fun/ ",
        "Seleccione todo, borre",
        "Click derecho, pegar",
        "Listo, ya tiene el diagrama de flujo"
    \]

    if modo\_prompt == 'config\prompt\_upd\_0.md':
        print\("\nAhora el siguiente paso es crear un diagrama de flujo"\)
        while True:
            for instruccion in instrucciones:
                print\(instruccion\)
                input\("Presione Enter para continuar...\n"\)

            menu\_3\_0 = input\("¿Ya pudo realizar el procedimiento sugerido? \(S/N\): "\).upper\(\)
            if menu\_3\_0 == 'S':
                break
            print\("Por favor, intente nuevamente el procedimiento o solicite asistencia."\)


        # Aquí puedes incluir más instrucciones relacionadas con la creación del diagrama de flujo

    else:
        input\("Presione una tecla para salir"\)
```

### C:\AppServ\www\AnalizadorDeProyecto\src\ManiArch.py
```plaintext
#SCR/ManiArch.py
import os
from logs.config\_logger import configurar\_logging

logger = configurar\_logging\(\)

def filtrar\_archivos\_por\_extension\(archivos, extensiones\):
    """
    Filtra una lista de archivos, retornando aquellos que coinciden con las extensiones dadas,
    utilizando un conjunto para una búsqueda más eficiente.

    Args:
        archivos \(list of str\): Lista de nombres de archivos a filtrar.
        extensiones \(list of str\): Extensiones para usar en el filtrado.

    Returns:
        list of str: Lista de archivos filtrados que coinciden con las extensiones.
    """
    extensiones\_set = set\(extensiones\)  # Conversión a conjunto para una búsqueda más rápida
    return \[archivo for archivo in archivos if os.path.splitext\(archivo\)\[1\] in extensiones\_set\]

def listar\_archivos\(ruta, extensiones=None\):
    """
    Lista los archivos en una ruta dada, opcionalmente filtrando por extensiones.

    Args:
        ruta \(str\): Ruta del directorio a explorar.
        extensiones \(list of str, optional\): Extensiones para filtrar archivos. Si es None, lista todos los archivos.

    Returns:
        list of str: Lista de archivos encontrados.
        list of str: Estructura de directorio y archivos.
    """
    archivos\_encontrados = \[\]
    estructura = \[\]

    logger.debug\(f"Iniciando listado de archivos en la ruta: {ruta}"\)

    for raiz, \_, archivos in os.walk\(ruta\):
        if '.git' in raiz:  # Ignorar directorios .git
            continue

        nivel = raiz.replace\(ruta, ''\).count\(os.sep\)
        indentacion = ' ' \* 4 \* nivel
        estructura.append\(f"{indentacion}{os.path.basename\(raiz\)}/"\)
        subindentacion = ' ' \* 4 \* \(nivel + 1\)

        archivos\_en\_raiz = \[os.path.join\(raiz, archivo\) for archivo in archivos\]
        archivos\_filtrados = archivos\_en\_raiz if extensiones is None else filtrar\_archivos\_por\_extension\(archivos\_en\_raiz, extensiones\)
        estructura.extend\(f"{subindentacion}{os.path.basename\(archivo\)}" for archivo in archivos\_filtrados\)
        archivos\_encontrados.extend\(archivos\_filtrados\)

    logger.debug\(f"Listado de archivos completo. Total de archivos encontrados: {len\(archivos\_encontrados\)}"\)

    return archivos\_encontrados, estructura

```

### C:\AppServ\www\AnalizadorDeProyecto\src\Principal.py
```plaintext
#SCR/Principal.py
import os
import time
import threading
import sys
from importlib import metadata
from ManiArch import listar\_archivos
from SalidDatos import generar\_archivo\_salida
from UtilSist import obtener\_version\_python, limpieza\_pantalla
from InterfazHM import  menu\_0,menu\_1, menu\_2,menu\_3 #, menu\_4
from logs.config\_logger import configurar\_logging


# Configuración del logger
logger = configurar\_logging\(\)
def obtener\_ruta\_analisis\(ruta\_proyecto\):
    ruta\_default = obtener\_ruta\_default\(\)
    logger.info\(f"Directorio por defecto: {ruta\_default}"\)
    respuesta = input\("¿Desea analizar el directorio por defecto? \(S/N\): "\).upper\(\)
    if respuesta == 'N':
        nueva\_ruta = menu\_0\(\)  # Solicita al usuario una nueva ruta
        if nueva\_ruta \!= ruta\_default:
            guardar\_nueva\_ruta\_default\(nueva\_ruta\)
        return nueva\_ruta
    return ruta\_default

def guardar\_nueva\_ruta\_default\(nueva\_ruta\):
    archivo\_default = 'config/path.txt'
    try:
        with open\(archivo\_default, 'w', encoding='utf-8'\) as file:
            file.write\(nueva\_ruta\)
        logger.info\(f"Nueva ruta por defecto guardada: {nueva\_ruta}"\)
    except IOError as e:
        logger.error\(f"Error al guardar la nueva ruta por defecto: {e}"\)

def main\(\):
    ruta\_proyecto = inicializar\(\) #############################
    ruta = obtener\_ruta\_analisis\(ruta\_proyecto\)
    print\("\n\nruta: ",ruta,"\n\n"\)
    if ruta and validar\_ruta\(ruta\):
        modo\_prompt = seleccionar\_modo\_operacion\(\)
        procesar\_archivos\(ruta, modo\_prompt, ruta\_proyecto\)
        realizar\_pasos\_adicionales\(modo\_prompt, ruta\)

def seleccionar\_modo\_operacion\(\):
    """
    Permite al usuario seleccionar el modo de operación y devuelve el prompt correspondiente.
    """
    return menu\_1\(\)

def realizar\_pasos\_adicionales\(modo\_prompt, ruta\):
    """
    Realiza pasos adicionales basados en el modo de operación seleccionado.
    """
    menu\_2\(modo\_prompt, ruta\)
    menu\_3\(modo\_prompt, ruta\)

def inicializar\(\):
    """
    Inicializa el entorno del script.

    Limpia la pantalla, muestra la versión de Python en uso y calcula la ruta del proyecto
    basándose en la ubicación del script actual. Imprime y devuelve la ruta del proyecto.

    Returns:
        str: La ruta del proyecto.
    """
    limpieza\_pantalla\(\)
    bienvenida\(\)
    logger.debug\(f"Versión de Python en uso: {obtener\_version\_python\(\)}"\)
    ruta\_script = os.path.dirname\(os.path.abspath\(\_\_file\_\_\)\)
    ruta\_proyecto = os.path.normpath\(os.path.join\(ruta\_script, ".."\)\)
    return ruta\_proyecto

def bienvenida\(\):
    mensaje = """Bienvenido al AnalizadorDeProyecto 🌟\nEste software es una herramienta avanzada diseñada para ayudarte a analizar, documentar y mejorar la estructura de tus proyectos de software...\n    ¡Esperamos que disfrutes utilizando esta herramienta y que te sea de gran ayuda en tus proyectos de software\!\n\n\nPresiona Enter para continuar...\n"""

    mostrar\_todo = False

    # Función que maneja la visualización del mensaje
    def mostrar\_mensaje\(\):
        nonlocal mostrar\_todo
        for caracter in mensaje:
            if mostrar\_todo:
                print\(mensaje\[mensaje.index\(caracter\):\], end='', flush=True\)
                break
            print\(caracter, end='', flush=True\)
            time.sleep\(0.05\)  # Ajusta este valor según sea necesario
        print\(\)  # Asegura una nueva línea después del mensaje

    # Thread para mostrar el mensaje
    hilo\_mensaje = threading.Thread\(target=mostrar\_mensaje\)
    hilo\_mensaje.start\(\)

    # Espera a que el usuario presione Enter
    input\(\)
    mostrar\_todo = True
    hilo\_mensaje.join\(\)  # Espera a que el hilo termine

    # Avanza a la siguiente etapa después de la segunda pulsación de Enter



def obtener\_ruta\_default\(\):
    """
    Obtiene la ruta por defecto desde un archivo de configuración.

    Intenta leer un archivo 'path.txt' ubicado en el directorio 'config' relativo al script actual.
    Si el archivo no existe, lo crea con un valor predeterminado y luego devuelve ese valor.

    Returns:
        str: La ruta por defecto leída del archivo o un valor predeterminado si el archivo no existe.
    """
    ruta\_script = obtener\_ruta\_script\(\)
    archivo\_default = os.path.join\(ruta\_script, '../config/path.txt'\)

    # Asegurarse de que el directorio 'config' exista
    os.makedirs\(os.path.dirname\(archivo\_default\), exist\_ok=True\)

    try:
        with open\(archivo\_default, 'r', encoding='utf-8'\) as file:
            return file.read\(\).strip\(\)
    except FileNotFoundError:
        # Especifica un valor más significativo o deja en blanco según tus necesidades
        valor\_por\_defecto = "Especifica\_tu\_ruta\_aquí"
        with open\(archivo\_default, 'w', encoding='utf-8'\) as file:
            file.write\(valor\_por\_defecto\)
        return valor\_por\_defecto

def obtener\_ruta\_script\(\):
    """
    Obtiene la ruta del directorio del script actual.

    Utiliza la variable mágica '\_\_file\_\_' para obtener la ruta completa del script en ejecución
    y luego extrae el directorio que lo contiene. Es útil para construir rutas relativas a la
    ubicación del script, independientemente del directorio de trabajo actual.

    Returns:
        str: Ruta del directorio donde se encuentra el script actual.
    """
    return os.path.dirname\(os.path.abspath\(\_\_file\_\_\)\)

def validar\_ruta\(ruta\):
    """
    Verifica si la ruta proporcionada es un directorio y si es accesible para lectura.

    Args:
        ruta \(str\): La ruta del directorio a validar.

    Returns:
        bool: True si la ruta es un directorio y es accesible para lectura, False en caso contrario.
    """
    # Verifica si la ruta es un directorio
    es\_directorio = os.path.isdir\(ruta\)

    # Verifica si el directorio es accesible para lectura
    es\_accesible = os.access\(ruta, os.R\_OK\)

    return es\_directorio and es\_accesible

def procesar\_archivos\(ruta, modo\_prompt, ruta\_archivos\):
    """
    Procesa los archivos en una ruta de proyecto dada.

    Args:
        ruta \(str\): Ruta a los archivos a procesar.
        modo\_prompt \(str\): Modo seleccionado para el procesamiento de archivos.
        ruta\_proyecto \(str\): Ruta al directorio del proyecto.

    Realiza operaciones de archivo basadas en el modo seleccionado y guarda la salida.
    """
    extensiones = \['.html', '.css', '.php', '.py', '.json', '.sql', '.md', '.txt'\]
    listar\_archivos\(ruta, extensiones\)
    return generar\_archivo\_salida\(ruta, modo\_prompt, extensiones, ruta\_archivos\)


if \_\_name\_\_ == "\_\_main\_\_":
    main\(\)

```

### C:\AppServ\www\AnalizadorDeProyecto\src\UtilSist.py
```plaintext
#SCR/UtilSist.py
import sys
from importlib import metadata
import os
from logs.config\_logger import configurar\_logging

# Configuración del logger
logger = configurar\_logging\(\)

def obtener\_version\_python\(\):
    return sys.version

def limpieza\_pantalla\(habilitar=True\):
    """
    Limpia la pantalla de la consola, si está habilitado.

    Args:
        habilitar \(bool\): Indica si la función de limpieza está habilitada.
    """
    if not habilitar:
        logger.debug\("Limpieza de pantalla deshabilitada."\)
        return

    try:
        if os.name == 'nt':
            os.system\('cls'\)
        else:
            os.system\('clear'\)
        logger.debug\("Pantalla limpiada."\)
    except Exception as e:
        logger.error\(f"No se pudo limpiar la pantalla: {e}"\)

```

### C:\AppServ\www\AnalizadorDeProyecto\src\logs\config_logger.py
```plaintext
#src/logs/config\_logger.py
import logging
from logging.handlers import RotatingFileHandler
import datetime
import os

class InfoErrorFilter\(logging.Filter\):
    def filter\(self, record\):
        # Permitir solo registros de nivel INFO y ERROR
        return record.levelno in \(logging.INFO, logging.ERROR\)

def configurar\_logging\(nivel=logging.INFO\):
    logger = logging.getLogger\(\)
    if logger.hasHandlers\(\):
        return logger

    # Configuración básica
    filename = 'src/logs/sistema.log'
    format = '%\(asctime\)s - %\(levelname\)s - %\(module\)s - %\(filename\)s:%\(lineno\)d: %\(message\)s'
    maxBytes = 10485760  # 10MB
    backupCount = 5
    formatter = logging.Formatter\(format\)

    # File Handler
    file\_handler = RotatingFileHandler\(filename, maxBytes=maxBytes, backupCount=backupCount\)
    file\_handler.setLevel\(logging.DEBUG\)
    file\_handler.setFormatter\(formatter\)

    # Console Handler con filtro personalizado
    console\_handler = logging.StreamHandler\(\)
    console\_handler.addFilter\(InfoErrorFilter\(\)\)  # Aplicar el filtro
    console\_handler.setFormatter\(formatter\)

    logger.setLevel\(nivel\)
    logger.addHandler\(file\_handler\)
    logger.addHandler\(console\_handler\)

    logger.info\("\n\n--------------- Nueva Sesión - {} - Nivel de Registro: {} ---------------\n\n".format\(
        datetime.datetime.now\(\).strftime\("%Y-%m-%d %H:%M:%S"\), logging.getLevelName\(logger.getEffectiveLevel\(\)\)\)\)

    return logger

# Configurar el logger con un nivel específico
configurar\_logging\(nivel=logging.DEBUG\)

```
