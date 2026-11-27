-- primario.sql
-- Prepara N2 para que N3 se copie de él (issue #19). Se corre una vez en el primario
-- y se puede repetir sin romper nada. El usuario y la contraseña salen del .env.

\getenv usuario POSTGRES_REPLICACION_USER
\getenv clave POSTGRES_REPLICACION_PASSWORD

-- 1. Usuario que solo puede replicar: no puede leer ni cambiar tablas.
SELECT format('CREATE ROLE %I WITH REPLICATION LOGIN PASSWORD %L', :'usuario', :'clave')
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'usuario')
\gexec

-- 2. Slot: el primario guarda los cambios hasta que N3 los recibe, aunque N3 se apague.
SELECT pg_create_physical_replication_slot('replica_n3')
WHERE NOT EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = 'replica_n3');

SELECT rolname, rolreplication FROM pg_roles WHERE rolname = :'usuario';
SELECT slot_name, active FROM pg_replication_slots;