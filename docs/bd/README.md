# Base de datos

Documentación de la base relacional distribuida (lineamientos IV-a). El código SQL vive en `db/`; aquí va la explicación y la evidencia.

| Documento (nombre sugerido) | Contenido | Lineamiento | Issue | Responsable |
| --- | --- | --- | --- | --- |
| `requerimientos.md` | Análisis de requerimientos y consultas frecuentes | IV-a1 | #5 | Arturo |
| `modelo-relacional.md` | Diagrama y explicación del esquema normalizado (llaves, índices) | IV-a2 | #5 | Arturo |
| `fragmentacion.md` | Fragmentación por zona, esquema de asignación y directorio de fragmentos | IV-a4 | #12 | Arturo |
| `replicacion.md` | Configuración primario-secundario y resultado de la prueba de falla | IV-a5 | #19, #25 | Arturo |
| `seguridad-bd.md` | Usuarios, roles, privilegios, TLS, cifrado en reposo y enmascaramiento | IV-a7 | #33 | Arturo |
| `monitoreo-respaldos.md` | Monitoreo de nodos, respaldo y recuperación | IV-a6 | #32, #39 | Hugo y Arturo |
| `mongodb.md` | Base analítica: colecciones y ETL | IV-a8 | #29 | Tadeo |

## Cómo se entrega

- Cada documento llega en el PR de su issue, junto con el código que describe.
- Las capturas que lo respalden van en `docs/evidencias/` y se enlazan desde aquí.
- Las decisiones (por qué zona, postura CAP) no se justifican aquí: van en `docs/decisiones/`.
