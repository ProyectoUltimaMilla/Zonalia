# db

Código SQL de PostgreSQL y catálogos (lineamientos IV-a). Responsable principal: Arturo.

| Carpeta | Contenido | Issue | Responsable |
| --- | --- | --- | --- |
| `esquema/` | Tablas, llaves e índices (`01_tablas.sql`, …), luego procedimientos, funciones y triggers | #5, #11 | Arturo |
| `catalogos/` | Catálogo de colonias de Aguascalientes, zonas y sus scripts de preparación y asignación | #9 | Tadeo |
| Replicación, roles y respaldos | Se agregan en sus issues | #19, #33, #39 | Arturo |

- La explicación de cada parte va en `docs/bd/`.
- Nunca se suben contraseñas: los scripts las leen de variables de entorno (`.env`).
