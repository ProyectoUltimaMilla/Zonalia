-- 003_historial.sql
-- Columnas y tabla que necesitan los triggers del issue #11.
-- Depende de 001_tablas.sql.

-- Fecha de la última modificación del paquete; la mantiene el trigger paquete_fecha_actualizacion.
ALTER TABLE paquete ADD COLUMN actualizado_en timestamptz NOT NULL DEFAULT now();

-- Cada cambio de estado de un paquete queda aquí (lo llena el trigger paquete_historial).
CREATE TABLE paquete_historial (
    historial_id     bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    zona_id          smallint    NOT NULL,
    paquete_id       bigint      NOT NULL,
    estado_anterior  text,                                 -- vacío cuando el paquete recién se registra
    estado_nuevo     text        NOT NULL,
    cambiado_por     bigint      REFERENCES usuario (usuario_id),  -- la API lo indica con SET LOCAL zonalia.usuario_id
    cambiado_en      timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (zona_id, paquete_id) REFERENCES paquete (zona_id, paquete_id) ON DELETE CASCADE
);

-- C4. Historial de un paquete en orden.
CREATE INDEX paquete_historial_paquete_idx ON paquete_historial (zona_id, paquete_id, cambiado_en);