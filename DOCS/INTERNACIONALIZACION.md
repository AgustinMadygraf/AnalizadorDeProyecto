# Guía de Internacionalización (i18n)

## ¿Cómo funciona?
Todos los textos de interacción con el usuario (menús, prompts, errores, ayuda) se gestionan desde archivos de idioma JSON en `src/common/i18n/`.

- Español: `es.json`
- Inglés: `en.json`

La variable de entorno `ANALIZADOR_LANG` define el idioma activo (`es` por defecto).

## ¿Cómo agregar o modificar mensajes?
1. Edita el archivo de idioma correspondiente (`es.json`, `en.json`).
2. Usa la misma clave en todos los idiomas.
3. Si agregas un nuevo mensaje en el código, crea la clave en ambos archivos.

## Ejemplo de clave
```json
"prompt_include_todo": "¿Desea incluir el análisis de 'todo.txt'? (S/N): "
```

## Buenas prácticas
- Nunca escribas textos duros en el código: usa siempre `LANG.get('clave', 'fallback')`.
- Mantén sincronizados los archivos de idioma.
- Si contribuyes un nuevo idioma, copia primero `es.json` y traduce.

## Cambiar idioma
En consola:
- Español: `set ANALIZADOR_LANG=es` (Windows) o `export ANALIZADOR_LANG=es` (Linux/macOS)
- Inglés: `set ANALIZADOR_LANG=en` o `export ANALIZADOR_LANG=en`

## Contacto
Si encuentras un mensaje sin traducir, abre un issue o contribuye la traducción.
