# Replicación primario-secundario (#19)

N2 (primario) envía cada cambio a N3 (réplica) en vivo por la VPN (*streaming replication* de PostgreSQL 16). N3 tiene la base completa y se puede consultar, pero no acepta escrituras.

## Cómo está armada

- **Usuario `replicador`**: solo tiene el permiso `REPLICATION`; no puede leer ni cambiar tablas. Su contraseña vive en el `.env` de N2 y de N3, nunca en el repo.
- **Slot `replica_n3`**: N2 guarda los cambios hasta que N3 los recibe, aunque N3 se apague un rato.
- **`pg_hba.conf` propio** (`db/replicacion/`): todo lo que llega por red pide contraseña con scram-sha-256. Docker Desktop no deja ver la IP real de quien se conecta, así que el filtro por IP está en el puerto: se publica solo en la IP de la VPN del nodo.
- **Tipo**: síncrona, según el ADR-002 (CP). N2 no confirma un cambio hasta que N3 lo tiene; se activa con `synchronous_standby_names = '*'` en N2.

## Cómo se arma

1. N2: `docker compose --profile n2 up -d db` con `IP_PUBLICACION_DB=10.10.0.2` y luego `db/replicacion/primario.sql`.
2. N3: `pg_basebackup` con `docker compose --profile n3 run …` y luego `docker compose --profile n3 up -d db-replica`.
3. Estado en cualquiera de los dos: `db/replicacion/estado.sql`.

## Resultados

Ensayo del 26 de noviembre con las dos bases en una sola laptop (evidencia en `docs/evidencias/issue-19/`). La prueba entre laptops por la VPN se agrega el 30 de noviembre.

| Prueba | Ensayo en una laptop (26 nov) |
| --- | --- |
| `pg_stat_replication` en el primario | La réplica aparece en `streaming` |
| Un INSERT en el primario | Aparece en la réplica en menos de un segundo |
| Un DELETE en la réplica | Rechazado: `cannot execute DELETE in a read-only transaction` |
| Retraso durante la carga de 100 000 paquetes (asíncrona) | Máximo de 0.36 segundos y 9.8 MB pendientes |
| Paquetes en N3 al terminar | 100 000 |
| Tiempo por cambio confirmado | 0.59 ms asíncrona, 1.42 ms síncrona |
| N3 detenido con réplica síncrona | El cambio en N2 espera (191 s en la prueba) y se completa solo al volver N3 |

La prueba de falla (apagar N2 y promover N3) es el #25.
