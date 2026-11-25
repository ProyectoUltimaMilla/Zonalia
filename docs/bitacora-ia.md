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
| 2026-11-24 | Jesús | Claude | Esqueleto de servicios: pyproject, main.py con /health, prueba y README de entorno (nivel libre: configuración inicial) | Se aceptó con un cambio: main.py y test_health.py no pasaban ruff format (faltaban líneas en blanco antes de cada def y el salto de línea final); lo corregí con ruff format. Lo revisé línea por línea y confirmé en PyPI las 8 dependencias | ruff, ruff format, bandit, pytest con 100 % de cobertura, pip-audit sin vulnerabilidades y /health en el navegador | 083f6d2 |
| 2026-11-25 | Arturo | Claude | Redacción de la sección de turnos de CONTRIBUTING y de la casilla de decisión del equipo (#67, nivel libre) | Se aceptó el texto; el reparto de turnos y la regla de integración los decidió el equipo | Revisión de Arturo contra lo acordado y de Jesús en el PR | 473c048 |
| 2026-11-25 | Arturo | Claude | Redacción de la sección de turnos de CONTRIBUTING y de la casilla de decisión del equipo (#68, nivel libre) | Se aceptó el texto; el reparto de turnos y la regla de integración los decidió el equipo | Revisión de Arturo contra lo acordado y de Jesús en el PR | 431e2ed |