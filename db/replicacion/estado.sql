-- estado.sql
-- Muestra cómo va la replicación (issue #19). En N2 lista a N3 y su retraso;
-- en N3 dice si está en recuperación (es réplica) y hasta dónde ha aplicado.

SELECT pg_is_in_recovery() AS soy_replica;

-- Solo trae filas en el primario:
SELECT application_name, client_addr, state, sync_state,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn)) AS falta_por_aplicar,
       write_lag, flush_lag, replay_lag
FROM pg_stat_replication;

-- Solo trae filas en la réplica:
SELECT status, sender_host, last_msg_receipt_time
FROM pg_stat_wal_receiver;