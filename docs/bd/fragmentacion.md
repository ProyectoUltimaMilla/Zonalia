# Fragmentación de la base (#12)

## Fragmentación horizontal: un fragmento por zona

La tabla `paquete` está particionada por lista sobre `zona_id`. Cada zona tiene su partición:

| Zona | Partición | Paquetes (datos sintéticos, 100 000) |
| --- | --- | --- |
| 1 Centro | `paquete_z1_centro` | 9 199 |
| 2 Norte | `paquete_z2_norte` | 24 063 |
| 3 Oriente | `paquete_z3_oriente` | 25 689 |
| 4 Sur | `paquete_z4_sur` | 21 881 |
| 5 Poniente | `paquete_z5_poniente` | 19 168 |

`paquete_sin_zona` (partición DEFAULT) queda vacía; solo recibiría paquetes de una zona nueva que todavía no tenga partición.

**Esquema de asignación:** cada paquete va al fragmento de la zona de su colonia. La zona sale del catálogo de colonias (`db/catalogos/`, #9) con la función `zona_de_colonia` (#11). La llave primaria `(zona_id, paquete_id)` incluye la zona, por eso PostgreSQL acepta la partición.

**Por qué conviene:** las consultas del día filtran por zona (paquetes por asignar, rutas y entregas pendientes de una cuadrilla). Con `WHERE zona_id = 3`, PostgreSQL solo lee `paquete_z3_oriente` (poda de particiones, captura del `EXPLAIN` en `docs/evidencias/issue-12/`).

## Fragmentación vertical: el destinatario aparte

Los datos personales del destinatario (nombre, teléfono, calle) viven en la tabla `destinatario`, separados de `paquete` y con la misma llave. Así se pueden cifrar y restringir (#33) sin tocar lo que usa la operación.

## Directorio de fragmentos

La tabla `directorio_fragmentos` dice en qué partición y en qué nodo vive cada zona. Se llena con `db/fragmentos/directorio.sql` después de cargar las zonas. Hoy las 5 zonas viven en N2 (primario) y se copian completas a N3 (réplica, #19).

## Cómo se reproduce

1. `docker compose --profile local down -v` y `docker compose --profile local up -d db`: PostgreSQL crea las tablas y las 5 particiones.
2. `python -m zonalia.generador --cargar`, desde `servicios`.
3. `docker compose exec -T db psql -U zonalia_admin -d zonalia -f - < db/fragmentos/directorio.sql`.

La decisión de fragmentar por zona y sus alternativas están en `docs/decisiones/ADR-001-shard-key.md`.