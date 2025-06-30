# Documentación Arquitectónica - AnalizadorDeProyecto

## 1. Visión General
El proyecto sigue los principios de Clean Architecture, separando responsabilidades en capas bien definidas para maximizar la mantenibilidad, testabilidad y escalabilidad.

## 2. Estructura de Carpetas

- `src/`
  - `common/`: Utilidades transversales puras (sin dependencias externas)
  - `domain/`: Lógica de negocio pura (ej: `report_generator.py`)
  - `application/`: Orquestación de casos de uso y lógica de aplicación (ej: `main_app.py`)
  - `infrastructure/`: Adaptadores a sistemas externos y utilidades técnicas (ej: `file_manager.py`, `logger_adapter.py`)
    - `file_adapters/`: Manejadores concretos de archivos (ej: `python_file_handler.py`)
  - `interfaces/`: Definición de puertos (interfaces) para la comunicación entre capas
  - `presentation/`: Lógica de presentación e interacción con el usuario (ej: CLI, UI)

- `tests/`
  - `domain/`, `application/`, `infrastructure/`, `presentation/`: Tests organizados por capa

## 3. Principios Clave
- **Independencia de frameworks:** El dominio y la aplicación no dependen de detalles de infraestructura.
- **Inversión de dependencias:** Las dependencias siempre apuntan hacia el dominio.
- **Separación de responsabilidades:** Cada capa tiene un propósito claro y único.
- **Testabilidad:** La lógica de negocio y de aplicación puede testearse de forma aislada.

## 4. Flujo de Dependencias

```
[presentation] → [application] → [domain] ← [infrastructure]
```
- La UI (CLI, web, etc.) interactúa con la capa de aplicación.
- La aplicación orquesta los casos de uso y delega en el dominio.
- El dominio define la lógica y las interfaces (puertos).
- La infraestructura implementa adaptadores concretos para los puertos definidos en el dominio.

## 5. Ejemplo de Caso de Uso
- El usuario ejecuta un comando en la UI (presentation).
- La UI llama a un caso de uso en la aplicación.
- La aplicación utiliza puertos para interactuar con el dominio.
- El dominio ejecuta la lógica y las interfaces (puertos).
- **El logging está desacoplado:** la aplicación emite eventos de log a través del puerto `LoggerEventPort`, y la infraestructura (`LoggerAdapter`) los registra. La aplicación nunca invoca métodos de logging concretos.
- La infraestructura implementa adaptadores concretos para los puertos definidos en el dominio.

## 5b. Inyección de Factory de Handlers de Archivos
- El dominio ya no instancia ni conoce adaptadores concretos de archivos.
- Se define el puerto `FileHandlerFactoryPort` en `interfaces/`.
- La infraestructura implementa `FileHandlerFactoryAdapter`, que conoce los handlers concretos.
- El entrypoint crea el factory y lo inyecta a `FileManager`.
- `FileManager` usa el factory para obtener el handler adecuado según la extensión, cumpliendo inversión de dependencias.

## 5c. Inyección de dependencias global (entrypoint)
- La creación de adaptadores concretos (implementaciones de puertos) se realiza exclusivamente en el entrypoint (`run.py`).
- El entrypoint instancia los adaptadores y los inyecta a la capa de aplicación mediante los puertos definidos en `interfaces/`.
- Ningún archivo de `application/` debe importar adaptadores concretos; solo puertos/interfaces.
- Este patrón garantiza el desacoplamiento y permite cambiar implementaciones sin modificar la lógica de aplicación.

### Ejemplo:
```python
# run.py
from src.infrastructure.file_manager_adapter import PythonFileManagerAdapter
from src.application.main_app import run_app

file_manager_adapter = PythonFileManagerAdapter()
run_app(file_manager_port=file_manager_adapter, ...)
```

- La política de inyección de dependencias debe mantenerse y validarse en futuras evoluciones del sistema.

## 6. Inyección de dependencias y puertos

La inyección de dependencias se realiza manualmente en `src/presentation/cli_entry.py`, donde se instancian los adaptadores concretos y se pasan a los orquestadores como puertos (interfaces). Esto asegura el cumplimiento del principio de inversión de dependencias y facilita el testeo y la extensión del sistema. Ejemplo:

```python
from src.infrastructure.logger_adapter import LoggerAdapter
logger_port = LoggerAdapter()
logger_event_port = logger_port  # LoggerAdapter implementa ambos puertos
```

Todos los adaptadores implementan explícitamente los puertos requeridos definidos en `src/interfaces/`.

## 7. Tests
- Los tests están organizados por capa, permitiendo validar cada responsabilidad de forma aislada.
- Se recomienda mantener mocks/adaptadores dobles para aislar dependencias externas en los tests de dominio y aplicación.

## 8. Estado Actual
- La migración a Clean Architecture está completa.
- El dominio está completamente desacoplado de la infraestructura (incluyendo manejo de archivos).
- El logging está desacoplado mediante el puerto `LoggerEventPort` y adaptadores concretos.
- La UI y la lógica de aplicación están separadas.
- El código duplicado ha sido eliminado.
- Los tests están organizados por capas y las utilidades puras se encuentran en `src/common/`.
- La inyección de dependencias para handlers de archivos se realiza vía factory, cumpliendo Clean Architecture.

## 9. Próximos Pasos
- Revisar y mejorar la cobertura de tests.
- Mantener la documentación actualizada ante futuros cambios estructurales.
