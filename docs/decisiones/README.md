# Registro de decisiones

Las decisiones importantes de diseño se documentan aquí, una por archivo, con contexto, alternativas, decisión y justificación con datos del propio sistema (apartado 5.3). Estas decisiones las toma el equipo; la IA solo puede listar alternativas (5.2: delegarlas a la IA es falta de integridad académica).

| ADR | Decisión | Issue | Responsable | Estado |
| --- | --- | --- | --- | --- |
| [ADR-001](ADR-001-shard-key.md) | Fragmentación y shard key | #12 | Arturo | Propuesta (Arturo, 26 nov) |
| [ADR-002](ADR-002-cap.md) | Postura CAP y tipo de consistencia | #12 | Arturo | Propuesta (Arturo, 26 nov) |
| [ADR-003](ADR-003-nodos.md) | Distribución de nodos | #18 | Arturo | Pendiente (se decide el 30 nov) |
| ADR-004 | Replicación y elección del nuevo primario | #25 | Arturo | Pendiente |
| ADR-005 | Principales controles de seguridad | #34 | Arturo | Pendiente |
| [ADR-006](ADR-006-estado-persistencia-flutter.md) | Estado y persistencia local en Flutter | #14 | Jesús | Propuesta |

## Cómo se hace un ADR

1. Copia [plantilla.md](plantilla.md) como `ADR-00N-tema-corto.md` (el número sigue la tabla de arriba).
2. Llena **Contexto** y **Alternativas** con datos del sistema: conteos del generador, consultas frecuentes, tiempos medidos. Sin datos no se acepta.
3. Discútelo con el equipo. La **Decisión** y la **Justificación** las escribe el equipo con sus palabras.
4. Ábrelo en un PR ligado al issue de la tabla. Lo aprueban los integrantes indicados en el issue; quienes aprueben se anotan en "Aprobada por".
5. Al integrarse, cambia el **Estado** a "Aceptada" en el archivo y en la tabla de arriba.
6. Si después cambia la decisión, no borres el ADR: crea uno nuevo y marca el viejo como "Reemplazada por ADR-00X".
