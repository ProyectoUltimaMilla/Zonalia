-- 006_triggers.sql
-- Triggers de paquete (issue #11): validan cada cambio de estado, guardan la fecha
-- de actualización y dejan el historial. Depende de 001_tablas.sql y 003_historial.sql.
--
-- Cambios de estado permitidos:
--   recibido  -> asignado
--   asignado  -> en_ruta | recibido (se quita de la ruta)
--   en_ruta   -> entregado | fallido
--   fallido   -> asignado (otro intento) | devuelto
--   entregado y devuelto son finales.

-- 1. Rechaza un cambio de estado que no está en la lista.
CREATE FUNCTION validar_transicion_paquete()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.estado IS DISTINCT FROM OLD.estado AND NOT (
           (OLD.estado = 'recibido' AND NEW.estado = 'asignado')
        OR (OLD.estado = 'asignado' AND NEW.estado IN ('en_ruta', 'recibido'))
        OR (OLD.estado = 'en_ruta'  AND NEW.estado IN ('entregado', 'fallido'))
        OR (OLD.estado = 'fallido'  AND NEW.estado IN ('asignado', 'devuelto'))
    ) THEN
        RAISE EXCEPTION 'Cambio de estado no permitido: % -> % (paquete %)',
            OLD.estado, NEW.estado, OLD.paquete_id
            USING ERRCODE = 'ZN003';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER paquete_validar_transicion
    BEFORE UPDATE OF estado ON paquete
    FOR EACH ROW EXECUTE FUNCTION validar_transicion_paquete();

-- 2. Pone la fecha de actualización en cada UPDATE.
CREATE FUNCTION poner_fecha_actualizacion()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.actualizado_en := now();
    RETURN NEW;
END;
$$;

CREATE TRIGGER paquete_fecha_actualizacion
    BEFORE UPDATE ON paquete
    FOR EACH ROW EXECUTE FUNCTION poner_fecha_actualizacion();

-- 3. Guarda en paquete_historial el alta y cada cambio de estado.
--    Quién lo hizo sale de zonalia.usuario_id, que la API fija con SET LOCAL en cada transacción.
CREATE FUNCTION registrar_historial_paquete()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF TG_OP = 'INSERT' OR NEW.estado IS DISTINCT FROM OLD.estado THEN
        INSERT INTO paquete_historial (zona_id, paquete_id, estado_anterior, estado_nuevo, cambiado_por)
        VALUES (
            NEW.zona_id, NEW.paquete_id,
            CASE WHEN TG_OP = 'UPDATE' THEN OLD.estado END,
            NEW.estado,
            nullif(current_setting('zonalia.usuario_id', true), '')::bigint
        );
    END IF;
    RETURN NULL;
END;
$$;

CREATE TRIGGER paquete_historial
    AFTER INSERT OR UPDATE OF estado ON paquete
    FOR EACH ROW EXECUTE FUNCTION registrar_historial_paquete();