-- 004_funciones.sql
-- Funciones de consulta que usan la API y el procedimiento asignar_paquete (issue #11).
-- Depende de 001_tablas.sql.
--
-- Códigos de error propios de Zonalia (la API los traduce a sus excepciones del dominio, #20):
--   ZN001  el paquete ya está asignado o no se puede asignar en su estado
--   ZN002  el repartidor llegó a su capacidad del día     (RepartidorSaturadoError)
--   ZN003  cambio de estado no permitido
--   ZN004  la colonia no existe                           (ZonaNoEncontradaError)
--   ZN005  el paquete y el repartidor son de zonas distintas
--   ZN006  el paquete o el repartidor no existen

-- Zona a la que pertenece una colonia. Se usa al importar manifiestos (#22, #30).
CREATE FUNCTION zona_de_colonia(p_colonia_id integer)
RETURNS smallint
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_zona smallint;
BEGIN
    SELECT zona_id INTO v_zona FROM colonia WHERE colonia_id = p_colonia_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'La colonia % no existe en el catálogo', p_colonia_id
            USING ERRCODE = 'ZN004';
    END IF;
    RETURN v_zona;
END;
$$;

-- Cuántos paquetes lleva asignados un repartidor en un día (C3).
CREATE FUNCTION carga_repartidor(p_repartidor_id bigint, p_fecha date DEFAULT current_date)
RETURNS integer
LANGUAGE sql
STABLE
AS $$
    SELECT count(*)::integer
    FROM asignacion a
    JOIN ruta r ON r.ruta_id = a.ruta_id
    WHERE r.repartidor_id = p_repartidor_id
      AND r.fecha = p_fecha;
$$;