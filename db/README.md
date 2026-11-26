# db

Código SQL de PostgreSQL y catálogos (lineamientos IV-a). Responsable principal: Arturo.

| Carpeta | Contenido | Issue | Responsable |
| --- | --- | --- | --- |
| | `esquema/` | Tablas, llaves e índices (`001_tablas.sql`, `002_indices.sql`), luego historial, funciones, procedimiento y triggers (`003` a `006`) | #5, #11 | Arturo |
| `pruebas/` | Scripts que comprueban las reglas de la base (`011_asignacion.sql`) | #11 | Arturo |
| Replicación, roles y respaldos | Se agregan en sus issues | #19, #33, #39 | Arturo |

- La explicación de cada parte va en `docs/bd/`.
- Nunca se suben contraseñas: los scripts las leen de variables de entorno (`.env`).
