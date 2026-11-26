-- 005_asignar_paquete.sql
-- Procedimiento que asigna un paquete a la ruta del día de un repartidor (issue #11).
-- Depende de 001_tablas.sql, 003_historial.sql y 004_funciones.sql.
--
-- Qué garantiza:
--   1. Un paquete no se asigna dos veces: bloquea su fila (FOR UPDATE) y revisa su estado.
--   2. No se pasa la capacidad: bloquea al repartidor, así dos asignaciones al mismo
--      tiempo no pueden contar la misma carga.
--   3. El orden de entrega queda agrupado por colonia (código postal y nombre).
-- Si algo falla, lanza un error ZN00x y PostgreSQL deshace todo lo que hizo el procedimiento.

CREATE PROCEDURE asignar_paquete(
    p_zona_id        smallint,
    p_paquete_id     bigint,
    p_repartidor_id  bigint,
    p_asignado_por   bigint,
    p_fecha          date DEFAULT current_date
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_estado      text;
    v_zona_rep    smallint;
    v_capacidad   smallint;
    v_ruta_id     bigint;
BEGIN
    -- 1. Bloquear el paquete y revisar que se pueda asignar.
    SELECT estado INTO v_estado
    FROM paquete
    WHERE zona_id = p_zona_id AND paquete_id = p_paquete_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El paquete % de la zona % no existe', p_paquete_id, p_zona_id
            USING ERRCODE = 'ZN006';
    END IF;

    IF v_estado NOT IN ('recibido', 'fallido') THEN
        RAISE EXCEPTION 'El paquete % ya está %; no se puede asignar otra vez', p_paquete_id, v_estado
            USING ERRCODE = 'ZN001';
    END IF;

    -- 2. Bloquear al repartidor y revisar su zona y su capacidad.
    SELECT zona_id, capacidad_diaria INTO v_zona_rep, v_capacidad
    FROM repartidor
    WHERE usuario_id = p_repartidor_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El repartidor % no existe', p_repartidor_id
            USING ERRCODE = 'ZN006';
    END IF;

    IF v_zona_rep <> p_zona_id THEN
        RAISE EXCEPTION 'El repartidor % es de la zona %, el paquete de la zona %',
            p_repartidor_id, v_zona_rep, p_zona_id
            USING ERRCODE = 'ZN005';
    END IF;

    IF carga_repartidor(p_repartidor_id, p_fecha) >= v_capacidad THEN
        RAISE EXCEPTION 'El repartidor % ya tiene % paquetes, su capacidad del día',
            p_repartidor_id, v_capacidad
            USING ERRCODE = 'ZN002';
    END IF;

    -- 3. Buscar la ruta del día del repartidor o crearla.
    INSERT INTO ruta (zona_id, repartidor_id, fecha)
    VALUES (p_zona_id, p_repartidor_id, p_fecha)
    ON CONFLICT (repartidor_id, fecha) DO NOTHING;

    SELECT ruta_id INTO v_ruta_id
    FROM ruta
    WHERE repartidor_id = p_repartidor_id AND fecha = p_fecha;

    -- 4. Registrar la asignación al final de la ruta y marcar el paquete.
    INSERT INTO asignacion (zona_id, paquete_id, ruta_id, orden, asignado_por)
    VALUES (
        p_zona_id, p_paquete_id, v_ruta_id,
        (SELECT coalesce(max(orden), 0) + 1 FROM asignacion WHERE ruta_id = v_ruta_id),
        p_asignado_por
    );

    UPDATE paquete
    SET estado = 'asignado'
    WHERE zona_id = p_zona_id AND paquete_id = p_paquete_id;

    -- 5. Reordenar la ruta por colonia. Primero se recorren todos los números lejos
    --    (+1000) para que la regla UNIQUE (ruta_id, orden) no choque a media actualización.
    UPDATE asignacion SET orden = orden + 1000 WHERE ruta_id = v_ruta_id;

    UPDATE asignacion a
    SET orden = n.nuevo_orden
    FROM (
        SELECT a2.asignacion_id,
               row_number() OVER (ORDER BY c.codigo_postal, c.nombre, a2.asignado_en, a2.asignacion_id)
                   AS nuevo_orden
        FROM asignacion a2
        JOIN paquete p ON p.zona_id = a2.zona_id AND p.paquete_id = a2.paquete_id
        JOIN colonia c ON c.colonia_id = p.colonia_id
        WHERE a2.ruta_id = v_ruta_id
    ) n
    WHERE a.asignacion_id = n.asignacion_id;
END;
$$;