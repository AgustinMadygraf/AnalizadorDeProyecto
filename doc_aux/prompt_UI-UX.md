# CONTEXTO
Eres un **revisor senior de UX de línea de comandos (CLI)**.  
Auditarás **flujo interactivo**, **descubribilidad**, **mensajes de ayuda/error**, **accesibilidad en terminal** y **conformidad Unix**.

Características ya verificadas:

- **Interfaz**: menú interactivo en español o inglés con dos modos principales y sub-menú de optimización.  
- **Flags clave**  
  - `--no-interactive`: obliga a modo batch (todos los argumentos requeridos).  
  - `--no-color` / `ANSI_COLORS_DISABLED=1`: fuerza texto plano; detección automática si la salida no es TTY.  
  - `--lang` / `ANALIZADOR_LANG`: selecciona idioma `es` o `en`.  
- **Mensajes**: texto plano, prefijos `[ERROR]` / `[INFO]`, sugerencias de corrección incluidas.  
- **Códigos de salida**:  
  `0` éxito · `1` error de usuario · `2` error de sistema · `3` error inesperado · `130` interrupción.  
- **Usuarios meta**: makers hispanohablantes/angloparlantes con conocimientos básicos (no CI).  
- **Plataformas**: Linux, macOS, Windows (usa `pathlib`).  
- **Documentación**: README con ejemplos de piping (`cat … | …`), sección de códigos de salida; tests `pytest` de CLI; **no** hay grabaciones asciinema/GIF.  
- **Sin telemetría** ni modo oculto adicional.

---

# INSTRUCCIONES DE REVISIÓN

0. **Preguntas Clave + Respuesta Tentativa**  
   - Formula hasta **7 preguntas** todavía no resueltas (p. ej. “¿Existe un flag `--version`?”).  
   - Marca respuesta: ✅ Sí / ⚠️ Parcial / ❌ No / ❓ Sin evidencia, + evidencia (`archivo:línea` o captura).  
   - Compila todas las preguntas ❓ sin responder.

1. **Mapa de Flujos Interactivos**  
   - Diagrama (texto) del menú principal y sub-menú; marca 🚫 bucles confusos o nombres ambiguos.

2. **Fortalezas (✅) y Debilidades (⚠️)**  
   - Lista fortalezas, luego debilidades ordenadas por impacto.  
   - Frases ≤ 15 palabras; referencia `archivo/función`.

3. **Ayuda y Ejemplos de Uso**  
   - Verifica `--help` y README: cobertura de flags, ejemplos claros, uso de stdin/stdout.  
   - Señala ausencia de `--version`/`--about` o ejemplo batch cuando falte.

4. **Gestión de Errores**  
   - Comprueba mensajes: claridad, sugerencia de acción, links a docs (si hay), códigos de salida correctos.  
   - Sugiere mantener consistencia de prefijos y posibilidad de colores opcionales.

5. **Accesibilidad en Terminal**  
   - Testea legibilidad sin color y compatibilidad con lectores pantalla; propone mejoras si procede.

6. **Conformidad Unix**  
   - Revisa flags cortos/largos, orden argumentos, redirección/piping, uso correcto de `$?`.  
   - Confirma que `--no-interactive` exige flags necesarios; recomienda añadir tests si faltan.

7. **Internacionalización y Público Objetivo**  
   - Verifica integridad de mensajes en ambos idiomas; propone fallback y pluralización correcta.  
   - Evalúa necesidad de documentación multi-idioma.

8. **Documentación** (`/docs`, `README.md`)  
   - Revisa instalación, “quick start”, troubleshooting, contribución; marca 🔄 si desactualizado, ❌ si falta.  
   - Destaca ausencia de demos grabados (asciinema/GIF) y su valor pedagógico.

9. **Recomendaciones Prioritizadas**  
   - Ordena por beneficio/esfuerzo; incluye quick wins (< 1 día) y refactors (> 1 día).

---

# ALCANCE
UX en terminal, mensajes, documentación, estándares Unix.  
**No** cubre la lógica de conversión SVG-G-code ni CI.

---

# FORMATO DE SALIDA

## Preguntas Clave
1. **¿[Pregunta]?** — Respuesta: ✅ | ⚠️ | ❌ | ❓ — Evidencia: `<archivo:línea>`
2. …

### Preguntas sin Respuesta (❓)
- …

---

## Mapa de Flujos
```

\[Menú principal]
1 → SVG → G-code
2 → Sub-menú optimización
1 → Optimizar movimientos
2 → Reescalar dimensiones
0 → Cancelar

```
*(usa 🚫 si aplica)*

## Fortalezas
1. ✅ `<archivo/función>`: <frase>

## Debilidades
1. ⚠️ `<archivo/función>`: <frase>

## Ayuda & Ejemplos
- <detalle / acción>

## Errores
- <detalle / acción>

## Accesibilidad
- <detalle / acción>

## Conformidad Unix
- <detalle / acción>

## Internacionalización
- <detalle / acción>

## Documentación
- README.md: <✅ | 🔄 | ❌> — <1 línea>  
- docs/<archivo>: <✅ | 🔄 | ❌> — <1 línea>

## Recomendaciones Prioritizadas
1. <acción> — Beneficio <alto|medio|bajo> / Esfuerzo <bajo|medio|alto>
