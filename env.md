# Configuración del Entorno Virtual para AnalizadorDeProyecto

## Crear el Entorno Virtual

Para aislar las dependencias y configuraciones de nuestro proyecto `AnalizadorDeProyecto`, utilizaremos un entorno virtual llamado `analizador_env`. Sigue estos pasos para configurarlo:

1. **Crear el Entorno Virtual:**
   Abre una terminal y navega al directorio del proyecto. Ejecuta el siguiente comando para crear un entorno virtual:

   ```bash
   python -m venv analizador_env
   ```
   Esto creará una nueva carpeta llamada `analizador_env` en tu directorio actual.

## Activar el Entorno Virtual

Antes de trabajar en el proyecto, necesitas activar el entorno virtual:

2. **Activar en Windows:**
   En sistemas Windows, activa el entorno virtual con:

   ```bash
   analizador_env\Scripts\activate
   ```
   Verás el nombre del entorno (`analizador_env`) en tu línea de comandos, indicando que está activo.

## Instalar Dependencias

Con el entorno virtual activo, es hora de instalar las dependencias:

3. **Instalar desde `requirements.txt`:**
   Asegúrate de que tienes un archivo `requirements.txt` en tu directorio del proyecto y ejecuta:

   ```bash
   pip install -r requirements.txt
   ```
   Esto instalará todas las dependencias necesarias para `AnalizadorDeProyecto`.

## Trabajar en el Proyecto

Ahora puedes trabajar en tu proyecto con todas las dependencias instaladas en el entorno virtual.

## Desactivar el Entorno Virtual

4. **Desactivar el Entorno:**
   Una vez que hayas terminado de trabajar, puedes desactivar el entorno virtual con:

   ```bash
   deactivate
   ```
   Esto volverá a tu entorno global o a cualquier otro entorno que estuvieras utilizando anteriormente.
