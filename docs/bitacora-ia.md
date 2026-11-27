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

| 2026-11-25 | Tadeo | Claude | Scripts para limpiar el catálogo SEPOMEX y aplicar y revisar las zonas (nivel libre). El criterio de zonas lo decidió el equipo sin IA | Se aceptaron; revisé cada paso y lo corrí con el catálogo real | Revisé a mano 10 colonias contra el TXT y revisar_zonas.py dio 0 colonias sin zona | a1de9d0 |
## Registro

El commit es el hash del commit en la rama (se conserva porque integramos con merge commit).

| Fecha | Integrante | Herramienta | Propósito | Resultado (aceptado, modificado, descartado y por qué) | Verificación | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-23 | Arturo | Claude | #1: plantillas de issue y PR, README base, CONTRIBUTING, estructura del repositorio y guías de llenado de cada carpeta (nivel libre) | Se aceptaron con ajustes de Arturo a textos y nombres | Revisión de Arturo contra los lineamientos y de Jesús en el PR de cimientos | d22699a |
| 2026-11-23 | Arturo | Claude | Plan de trabajo, lista de 56 issues y script para crearlos en GitHub (nivel libre: configuración inicial) | Se aceptó el plan después de ajustar el calendario; los issues se crearon tal como están en el plan | Revisión de Arturo de cada issue y verificación de que los números coinciden con el plan | No aplica (configuración en GitHub) |
| 2026-11-24 | Arturo | Claude | Compose con perfiles por nodo, Dockerfile de la API y Nginx básico (#6, nivel con verificación) | Se aceptó la estructura de perfiles. Se dejó que la API no espere a la base en el nodo 1 (required: false) y que la base solo escuche en la máquina hasta tener VPN | db y mongo en estado healthy con el perfil local; cada perfil lista sus servicios; git grep no encontró contraseñas | 782f3ad |
| 2026-11-24 | Jesús | Claude | Esqueleto de servicios: pyproject, main.py con /health, prueba y README de entorno (nivel libre: configuración inicial) | Se aceptó con un cambio: main.py y test_health.py no pasaban ruff format (faltaban líneas en blanco antes de cada def y el salto de línea final); lo corregí con ruff format. Lo revisé línea por línea y confirmé en PyPI las 8 dependencias | ruff, ruff format, bandit, pytest con 100 % de cobertura, pip-audit sin vulnerabilidades y /health en el navegador | 083f6d2 |
| 2026-11-25 | Arturo | Claude | Redacción de la sección de turnos de CONTRIBUTING y de la casilla de decisión del equipo (#68, nivel libre) | Se aceptó el texto; el reparto de turnos y la regla de integración los decidió el equipo | Revisión de Arturo contra lo acordado y de Jesús en el PR | 431e2ed |
| 2026-11-24 | Arturo | Claude | Esquema relacional, índices y documentos de requerimientos y modelo (#5, nivel con verificación) | Se aceptó el esquema. Se ajustó la llave foránea compuesta (colonia, zona) para que la zona del paquete no se contradiga y se dejó una partición por defecto hasta que se definan las zonas (#9, #12) | Se levantó PostgreSQL 16 con los scripts: 13 tablas creadas, el paquete cayó en su partición y la base rechazó un paquete con zona incorrecta. Al cruzarlo con el catálogo de SEPOMEX (#9) se cambió la regla única de colonia para incluir el tipo de asentamiento | 88d9c8d |
| 2026-11-25 | Arturo | Claude | Procedimiento asignar_paquete, funciones zona_de_colonia y carga_repartidor, triggers de transición, fecha e historial, y script de pruebas (#11, nivel con verificación) | Se aceptó con dos ajustes: bloquear también al repartidor para que dos asignaciones simultáneas no pasen la capacidad, y fijar los id de las pruebas para poder repetirlas | 011_asignacion.sql pasa los 8 casos dos veces seguidas; con el procedimiento renombrado la prueba falla; con dos terminales, la segunda asignación del mismo paquete espera el bloqueo y se rechaza con ZN001 | f6a4b9e |
| 2026-11-25 | Jesús | Claude | Workflow de CI con ruff, bandit, pytest con cobertura mínima y pip-audit (nivel libre) | Se aceptó; comprobé que el job se llama servicios | Check en verde en #63 y en rojo al quitar la prueba en #64 | d00c764 |
| 2026-11-25 | Jesús | Claude | Esqueleto Flutter: capas, Material 3, navegación adaptable, cliente HTTP con token y errores, pruebas, job app del CI y alternativas del ADR-006 (#14, nivel libre) | Se aceptó el código; la decisión del ADR-006 la revisé. Se corrigió la sangría del job app y se fijó Flutter 3.47.1 en el CI porque la versión estable 3.50.1 marca material.dart como obsoleto (la migración a material_ui queda para decisión del equipo) | flutter analyze sin problemas y flutter test con 6 pruebas en verde en el check app del CI. En mi compu Windows bloqueó la ejecución de Flutter (Access is denied), así que las pruebas en Chrome y en el emulador quedan pendientes | 74d6275 |
| 2026-11-25 | Jesús | Claude | Autenticación: login con JWT que expira, hash argon2, dependencia de rol, CORS y sus pruebas (#13, nivel con verificación) | Se aceptó con un cambio: los archivos no pasaban ruff format (faltaba el salto de línea final); lo corregí con ruff format. Lo revisé línea por línea y confirmé en PyPI argon2-cffi, pyjwt y psycopg | pytest con 10 pruebas en verde (login correcto, 401 por contraseña, usuario inexistente o dado de baja, token falso y expirado, 403 por rol y CORS), bandit y pip-audit sin hallazgos | 23af2e1 |
| 2026-11-26 | Hugo | ChatGPT | #10: orientación sobre activos, amenazas, escala CIA, riesgos R01 a R16, defensas y revisión documental (decisión del equipo) | Se utilizaron propuestas como apoyo; el integrante revisó y decidió los riesgos y las medidas de seguridad | Cálculos de probabilidad e impacto comprobados sobre el borrador, revisión del conteo de riesgos y correcciones solicitadas por Arturo. Revisado por Arturo en el PR | 1b7ec58, 1b99830, 3050543, 86ca4b7, eb149c0, 2e525e6, 79ed5f6, 5d58949 |
| 2026-11-26 | Hugo | ChatGPT | Correccion de documentacion y formato Markdown del entorno (#3, nivel libre) | Se acepto la orientacion para corregir la tabla de integrantes y el formato de la bitacora IA | Revision del README, inspeccion de la rama remota y git diff --check sin errores | 3cf5446, c9445c0 |
| 2026-11-26 | Hugo | ChatGPT | Middleware de bitácora de accesos en JSON, pruebas y documentación (#16, nivel con verificación) | Se aceptó el código y se revisó la integración con la autenticación, la exclusión de datos sensibles y la configuración local | Ruff, Bandit y pytest exitosos según ejecución del integrante; prueba en vivo con Uvicorn, registros JSON, respuestas HTTP 200 y 401 y exclusión de parámetros de consulta | c48c855, f7e53c7, 2e37c85 |
| 2026-11-26 | Hugo | ChatGPT | Orientación y revisión del marco legal de Zonalia (#17, decisión del equipo) | Se aceptaron ideas para identificar datos personales, analizar obligaciones legales, geolocalización, seguridad y datos sintéticos. El integrante tomó las decisiones y redactó el documento | Contraste con el esquema SQL, requerimientos de la base de datos y medidas de seguridad del proyecto. Verificación jurídica definitiva pendiente | 2af2f6c, 339024e, 49614c8 |
| 2026-11-26 | Tadeo | Claude | Generador de 100 mil registros sintéticos con Faker y semilla fija, manifiestos CSV y JSON, y carga a PostgreSQL con COPY (#15, nivel libre) | Se aceptó; se revisó que ningún dato sea real (destinatarios de Faker, colonias del catálogo público) y que nadie pase de 60 paquetes | pytest con 21 pruebas en verde (7 del generador); 100 000 paquetes cargados en el PostgreSQL del compose por Arturo y la misma cuenta por zona al recargar con la misma semilla | e728f04 |
