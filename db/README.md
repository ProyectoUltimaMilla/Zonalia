# db

Código SQL de PostgreSQL y catálogos (lineamientos IV-a). Responsable principal: Arturo.

| Carpeta | Contenido | Issue | Responsable |
| --- | --- | --- | --- |
| `esquema/` | Tablas, llaves e índices (`001`, `002`), historial, funciones, procedimiento y triggers (`003` a `006`) y particiones por zona (`007`). PostgreSQL los corre en orden la primera vez que arranca | #5, #11, #12 | Arturo |
| `fragmentos/` | `directorio.sql`: llena el directorio de fragmentos después de cargar los datos | #12 | Arturo |
| `pruebas/` | Scripts que comprueban las reglas de la base (`011_asignacion.sql`) | #11 | Arturo |
| `catalogos/` | Colonias de SEPOMEX con su zona y los scripts para regenerarlas | #9 | Tadeo |
| Replicación, roles y respaldos | `replicacion/`: pg_hba.conf, primario.sql y estado.sql (#19); roles y respaldos se agregan en sus issues | #19, #33, #39 | Arturo |

- La explicación de cada parte va en `docs/bd/`.
- Nunca se suben contraseñas: los scripts las leen de variables de entorno (`.env`).
