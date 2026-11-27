-- 011_asignacion.sql
-- Pruebas del issue #11: procedimiento asignar_paquete, funciones y triggers.
-- Se corre sobre una base recién creada con db/esquema. Todo pasa dentro de una
-- transacción que al final se deshace, así que no deja datos.
-- Cada prueba imprime "OK n: ..." y, si algo no se cumple, el script se detiene con "FALLA".
--
-- Uso:  psql -v ON_ERROR_STOP=1 -U postgres -f db/pruebas/011_asignacion.sql

\set QUIET on
BEGIN;

-- Datos de prueba (ficticios)
INSERT INTO zona (zona_id, nombre) VALUES (1, 'Centro'), (2, 'Norte');
INSERT INTO colonia VALUES
    (9001, '20000', 'Colonia A', 'Colonia', 1),
    (9002, '20010', 'Colonia B', 'Colonia', 1),
    (9003, '20100', 'Colonia C', 'Colonia', 2);
-- Los id se ponen a mano (OVERRIDING SYSTEM VALUE) para que el script se pueda
-- correr las veces que sea: el ROLLBACK borra los datos pero no regresa los contadores.
INSERT INTO paqueteria (paqueteria_id, nombre) OVERRIDING SYSTEM VALUE
VALUES (901, 'Paquetería de prueba');
INSERT INTO usuario (usuario_id, nombre_usuario, nombre_completo, hash_contrasena, rol)
OVERRIDING SYSTEM VALUE VALUES
    (901, 'sup1', 'Supervisor Prueba', 'x', 'supervisor'),
    (902, 'rep1', 'Repartidor Uno',    'x', 'repartidor'),
    (903, 'rep2', 'Repartidor Dos',    'x', 'repartidor');
INSERT INTO repartidor (usuario_id, zona_id, capacidad_diaria) VALUES (902, 1, 2), (903, 1, 10);
INSERT INTO manifiesto (manifiesto_id, paqueteria_id, fecha_recepcion, archivo_nombre, importado_por)
OVERRIDING SYSTEM VALUE VALUES (901, 901, current_date, 'prueba.csv', 901);
INSERT INTO paquete (paquete_id, zona_id, colonia_id, manifiesto_id, guia) OVERRIDING SYSTEM VALUE VALUES
    (901, 1, 9002, 901, 'P001'),   -- colonia B
    (902, 1, 9001, 901, 'P002'),   -- colonia A
    (903, 1, 9002, 901, 'P003'),   -- colonia B
    (904, 1, 9001, 901, 'P004'),   -- colonia A
    (905, 2, 9003, 901, 'P005');   -- zona 2

DO $$
DECLARE
    v_estado  text;
    v_n       integer;
    v_fecha   timestamptz;
    v_orden   text;
BEGIN
    -- 1. Funciones
    IF zona_de_colonia(9003) <> 2 THEN
        RAISE EXCEPTION 'FALLA 1: zona_de_colonia no devolvió la zona 2';
    END IF;
    BEGIN
        PERFORM zona_de_colonia(12345);
        RAISE EXCEPTION 'FALLA 1: zona_de_colonia aceptó una colonia que no existe';
    EXCEPTION WHEN SQLSTATE 'ZN004' THEN
        NULL;
    END;
    RAISE NOTICE 'OK 1: zona_de_colonia da la zona y rechaza colonias que no existen';

    -- 2. Asignación correcta
    CALL asignar_paquete(1::smallint, 901, 902, 901);
    SELECT estado INTO v_estado FROM paquete WHERE paquete_id = 901;
    IF v_estado <> 'asignado' OR carga_repartidor(902) <> 1 THEN
        RAISE EXCEPTION 'FALLA 2: el paquete no quedó asignado o la carga no es 1';
    END IF;
    RAISE NOTICE 'OK 2: el paquete queda asignado y carga_repartidor cuenta 1';

    -- 3. Un paquete no se asigna dos veces (ni al mismo ni a otro repartidor)
    BEGIN
        CALL asignar_paquete(1::smallint, 901, 903, 901);
        RAISE EXCEPTION 'FALLA 3: el paquete P001 se asignó dos veces';
    EXCEPTION WHEN SQLSTATE 'ZN001' THEN
        NULL;
    END;
    RAISE NOTICE 'OK 3: un paquete no se asigna dos veces';

    -- 4. No se pasa la capacidad (rep1 tiene capacidad 2)
    CALL asignar_paquete(1::smallint, 902, 902, 901);
    BEGIN
        CALL asignar_paquete(1::smallint, 903, 902, 901);
        RAISE EXCEPTION 'FALLA 4: se pasó la capacidad del repartidor';
    EXCEPTION WHEN SQLSTATE 'ZN002' THEN
        NULL;
    END;
    SELECT estado INTO v_estado FROM paquete WHERE paquete_id = 903;
    IF v_estado <> 'recibido' OR carga_repartidor(902) <> 2 THEN
        RAISE EXCEPTION 'FALLA 4: el intento fallido dejó cambios (rollback incompleto)';
    END IF;
    RAISE NOTICE 'OK 4: no se pasa la capacidad y el intento fallido no deja cambios';

    -- 5. Paquete de otra zona
    BEGIN
        CALL asignar_paquete(2::smallint, 905, 903, 901);
        RAISE EXCEPTION 'FALLA 5: se asignó un paquete de otra zona';
    EXCEPTION WHEN SQLSTATE 'ZN005' THEN
        NULL;
    END;
    RAISE NOTICE 'OK 5: no se asigna un paquete a un repartidor de otra zona';

    -- 6. Orden por colonia: cada repartidor recibió primero uno de la colonia B y luego uno de la A;
    --    la ruta debe quedar A, B
    CALL asignar_paquete(1::smallint, 903, 903, 901);
    CALL asignar_paquete(1::smallint, 904, 903, 901);
    SELECT string_agg(c.nombre, ', ' ORDER BY a.orden) INTO v_orden
    FROM asignacion a
    JOIN ruta r ON r.ruta_id = a.ruta_id
    JOIN paquete p ON p.zona_id = a.zona_id AND p.paquete_id = a.paquete_id
    JOIN colonia c ON c.colonia_id = p.colonia_id
    WHERE r.repartidor_id = 902;
    IF v_orden <> 'Colonia A, Colonia B' THEN
        RAISE EXCEPTION 'FALLA 6: orden de rep1 = %', v_orden;
    END IF;
    SELECT string_agg(c.nombre, ', ' ORDER BY a.orden) INTO v_orden
    FROM asignacion a
    JOIN ruta r ON r.ruta_id = a.ruta_id
    JOIN paquete p ON p.zona_id = a.zona_id AND p.paquete_id = a.paquete_id
    JOIN colonia c ON c.colonia_id = p.colonia_id
    WHERE r.repartidor_id = 903;
    IF v_orden <> 'Colonia A, Colonia B' THEN
        RAISE EXCEPTION 'FALLA 6: orden de rep2 = %', v_orden;
    END IF;
    RAISE NOTICE 'OK 6: la ruta queda ordenada por colonia';

    -- 7. Transición inválida: de asignado no se puede pasar directo a entregado
    BEGIN
        UPDATE paquete SET estado = 'entregado' WHERE paquete_id = 901;
        RAISE EXCEPTION 'FALLA 7: se aceptó asignado -> entregado';
    EXCEPTION WHEN SQLSTATE 'ZN003' THEN
        NULL;
    END;
    RAISE NOTICE 'OK 7: una transición inválida se rechaza';

    -- 8. Transición válida, fecha de actualización e historial
    SELECT actualizado_en INTO v_fecha FROM paquete WHERE paquete_id = 901;
    PERFORM set_config('zonalia.usuario_id', '902', true);
    UPDATE paquete SET estado = 'en_ruta' WHERE paquete_id = 901;
    IF (SELECT actualizado_en FROM paquete WHERE paquete_id = 901) < v_fecha THEN
        RAISE EXCEPTION 'FALLA 8: no cambió actualizado_en';
    END IF;
    SELECT count(*) INTO v_n FROM paquete_historial WHERE paquete_id = 901;
    IF v_n <> 3 THEN
        RAISE EXCEPTION 'FALLA 8: el historial del paquete P001 tiene % filas, se esperaban 3', v_n;
    END IF;
    IF (SELECT cambiado_por FROM paquete_historial
        WHERE paquete_id = 901 AND estado_nuevo = 'en_ruta') <> 902 THEN
        RAISE EXCEPTION 'FALLA 8: el historial no guardó quién hizo el cambio';
    END IF;
    RAISE NOTICE 'OK 8: historial (recibido, asignado, en_ruta) con fecha y usuario';
END;
$$;

ROLLBACK;
\echo 'Todas las pruebas del #11 pasaron.'