-- 007_fragmentos.sql
-- Fragmentación horizontal de paquete por zona (issue #12, ADR-001).
-- Depende de 001_tablas.sql. Una partición por zona; paquete_sin_zona (DEFAULT) queda
-- solo como red de seguridad para una zona nueva que todavía no tenga partición.
-- Los números de zona son los del catálogo del #9 (db/catalogos/zonas.csv).

CREATE TABLE paquete_z1_centro   PARTITION OF paquete FOR VALUES IN (1);
CREATE TABLE paquete_z2_norte    PARTITION OF paquete FOR VALUES IN (2);
CREATE TABLE paquete_z3_oriente  PARTITION OF paquete FOR VALUES IN (3);
CREATE TABLE paquete_z4_sur      PARTITION OF paquete FOR VALUES IN (4);
CREATE TABLE paquete_z5_poniente PARTITION OF paquete FOR VALUES IN (5);