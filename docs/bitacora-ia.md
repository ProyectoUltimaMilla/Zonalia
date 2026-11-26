# Bitácora de uso de IA

Se registran solo los usos que produjeron algo que se integró al proyecto o que influyeron en una decisión (apartado 5.3 de los lineamientos). La herramienta usada se registra en la columna Herramienta y coincide con la declarada en la carta de IA.

> Lineamientos 5.1: usar IA no se penaliza; ocultar su uso sí. Declarar el uso nunca resta puntos.

## Cómo se llena

1. **Cuándo:** solo si lo que te dio la IA terminó en tu PR o influyó en una decisión. Una pregunta que no usaste no se registra.
2. **Dónde:** agrega tu fila al final de la tabla, en la misma rama y el mismo PR del cambio. Nunca en un PR aparte.
3. **Columnas:**
   - **Fecha:** AAAA-MM-DD.
   - **Integrante:** tu nombre.
   - **Herramienta:** el asistente que usaste (de chat o del editor), igual que en la carta de IA.
   - **Propósito:** qué querías resolver y el nivel (libre, con verificación). Incluye el número de issue.
   - **Resultado:** qué aceptaste, qué cambiaste y qué descartaste, y por qué.
   - **Verificación:** cómo comprobaste que funciona y es seguro: prueba, comando, revisión o documentación oficial.
   - **Commit:** el hash corto del commit donde entró el cambio (`git log -1 --format=%h`). Como el commit se crea después de escribir la fila, primero haz el commit del cambio y luego un segundo commit que solo pone el hash en la bitácora.
4. **Commits:** el commit que trae código o texto de IA termina con la línea `IA: asistido` o `IA: generado y revisado` (5.3).
5. **Nivel con verificación** (SQL, triggers, replicación, firewall, TLS, VPN, criptografía, lógica de negocio): además de la fila, el PR debe traer pruebas que lo respalden y la revisión de otro integrante.
6. **No permitido** (5.2): que la IA decida fragmentación, shard key, postura CAP o análisis de riesgos, o que redacte conclusiones o el marco legal sin revisión. Esas decisiones van en `docs/decisiones/` y las escribe el equipo.

Ejemplo:

| Fecha | Integrante | Herramienta | Propósito | Resultado | Verificación | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-25 | Nombre | Asistente usado | #13: función para validar el token JWT (con verificación) | Se aceptó la estructura; se cambió el tiempo de expiración a 8 h | `pytest tests/test_auth.py` en verde y revisión de Hugo | a1b2c3d |

## Registro

El commit es el hash del commit en la rama (se conserva porque integramos con merge commit).

| Fecha | Integrante | Herramienta | Propósito | Resultado (aceptado, modificado, descartado y por qué) | Verificación | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-23 | Arturo | Claude | #1: plantillas de issue y PR, README base, CONTRIBUTING, estructura del repositorio y guías de llenado de cada carpeta (nivel libre) | Se aceptaron con ajustes de Arturo a textos y nombres | Revisión de Arturo contra los lineamientos y de Jesús en el PR de cimientos | d22699a |
| 2026-11-23 | Arturo | Claude | Plan de trabajo, lista de 56 issues y script para crearlos en GitHub (nivel libre: configuración inicial) | Se aceptó el plan después de ajustar el calendario; los issues se crearon tal como están en el plan | Revisión de Arturo de cada issue y verificación de que los números coinciden con el plan | No aplica (configuración en GitHub) |
| 2026-11-24 | Arturo | Claude | Compose con perfiles por nodo, Dockerfile de la API y Nginx básico (#6, nivel con verificación) | Se aceptó la estructura de perfiles. Se dejó que la API no espere a la base en el nodo 1 (required: false) y que la base solo escuche en la máquina hasta tener VPN | db y mongo en estado healthy con el perfil local; cada perfil lista sus servicios; git grep no encontró contraseñas | 782f3ad |
| 2026-11-24 | Jesús | Claude | Esqueleto de servicios: pyproject, main.py con /health, prueba y README de entorno (nivel libre: configuración inicial) | Se aceptó con un cambio: main.py y test_health.py no pasaban ruff format (faltaban líneas en blanco antes de cada def y el salto de línea final); lo corregí con ruff format. Lo revisé línea por línea y confirmé en PyPI las 8 dependencias | ruff, ruff format, bandit, pytest con 100 % de cobertura, pip-audit sin vulnerabilidades y /health en el navegador | 083f6d2 |
| 2026-11-24 | Arturo | Claude | Esquema relacional, índices y documentos de requerimientos y modelo (#5, nivel con verificación) | Se aceptó el esquema. Se ajustó la llave foránea compuesta (colonia, zona) para que la zona del paquete no se contradiga y se dejó una partición por defecto hasta que se definan las zonas (#9, #12) | Se levantó PostgreSQL 16 con los scripts: 13 tablas creadas, el paquete cayó en su partición y la base rechazó un paquete con zona incorrecta. Al cruzarlo con el catálogo de SEPOMEX (#9) se cambió la regla única de colonia para incluir el tipo de asentamiento | 88d9c8d |
| 2026-11-25 | Arturo | Claude | Procedimiento asignar_paquete, funciones zona_de_colonia y carga_repartidor, triggers de transición, fecha e historial, y script de pruebas (#11, nivel con verificación) | Se aceptó con dos ajustes: bloquear también al repartidor para que dos asignaciones simultáneas no pasen la capacidad, y fijar los id de las pruebas para poder repetirlas | 011_asignacion.sql pasa los 8 casos dos veces seguidas; con el procedimiento renombrado la prueba falla; con dos terminales, la segunda asignación del mismo paquete espera el bloqueo y se rechaza con ZN001 | f6a4b9e |
| 2026-11-25 | Jesús | Claude | Workflow de CI con ruff, bandit, pytest con cobertura mínima y pip-audit (nivel libre) | Se aceptó; comprobé que el job se llama servicios | Check en verde en #63 y en rojo al quitar la prueba en #64 | d00c764 |

