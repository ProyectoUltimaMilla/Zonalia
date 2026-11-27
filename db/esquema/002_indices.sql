-- 002_indices.sql
-- Índices para las consultas frecuentes descritas en docs/bd/requerimientos.md (issue #5).
-- Depende de 001_tablas.sql. Cada índice dice qué consulta atiende (C1 a C6).

-- C1. Paquetes por asignar de una zona, del más antiguo al más nuevo.
CREATE INDEX paquete_zona_estado_idx ON paquete (zona_id, estado, recibido_en);

-- C2. Buscar un paquete por su número de guía (al escanear o al confirmar).
CREATE INDEX paquete_guia_idx ON paquete (guia);

-- C3. Rutas del día y carga de cada repartidor en una zona.
CREATE INDEX ruta_fecha_zona_idx ON ruta (fecha, zona_id);

-- C4. Unir una asignación con su paquete (historial de un paquete).
CREATE INDEX asignacion_paquete_idx ON asignacion (zona_id, paquete_id);

-- C5. Entregas fallidas en un periodo, para el reporte por colonia.
CREATE INDEX entrega_fallida_fecha_idx ON entrega (registrada_en) WHERE resultado = 'fallido';

-- C6. Paquetes de un manifiesto (revisar una importación).
CREATE INDEX paquete_manifiesto_idx ON paquete (manifiesto_id);

-- Llaves foráneas que se consultan seguido.
CREATE INDEX colonia_zona_idx ON colonia (zona_id);
CREATE INDEX paquete_colonia_idx ON paquete (colonia_id);