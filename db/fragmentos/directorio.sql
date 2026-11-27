-- directorio.sql
-- Llena el directorio de fragmentos (issue #12): qué partición tiene cada zona y en qué
-- nodo vive. Se corre después de cargar las zonas (generador #15). Se puede repetir.
-- Hoy todas las zonas viven en N2 (primario) y se copian completas a N3 (réplica, #19).

INSERT INTO directorio_fragmentos (zona_id, particion, nodo_primario, nodo_replica)
SELECT z.zona_id, c.relname, 'n2', 'n3'
FROM zona z
JOIN pg_inherits i ON i.inhparent = 'paquete'::regclass
JOIN pg_class c ON c.oid = i.inhrelid
WHERE pg_get_expr(c.relpartbound, c.oid) = format('FOR VALUES IN (''%s'')', z.zona_id)
ON CONFLICT (zona_id) DO UPDATE
SET particion = EXCLUDED.particion,
    nodo_primario = EXCLUDED.nodo_primario,
    nodo_replica = EXCLUDED.nodo_replica,
    actualizado_en = now();

SELECT zona_id, particion, nodo_primario, nodo_replica FROM directorio_fragmentos ORDER BY zona_id;