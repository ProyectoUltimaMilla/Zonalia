-- 001_tablas.sql
-- Crea las tablas de Zonalia con sus llaves primarias, foráneas y restricciones (issue #5).
-- No depende de otro archivo. Las particiones por zona se crean en 007_fragmentos.sql (issue #12).

-- Catálogos

CREATE TABLE zona (
    zona_id   smallint PRIMARY KEY,
    nombre    text     NOT NULL UNIQUE,
    activa    boolean  NOT NULL DEFAULT true
);

CREATE TABLE colonia (
    colonia_id         integer  PRIMARY KEY,          -- id de SEPOMEX
    codigo_postal      char(5)  NOT NULL CHECK (codigo_postal ~ '^[0-9]{5}$'),
    nombre             text     NOT NULL,
    tipo_asentamiento  text     NOT NULL,
    zona_id            smallint NOT NULL REFERENCES zona (zona_id),
    UNIQUE (codigo_postal, nombre, tipo_asentamiento),   -- SEPOMEX repite nombres en un CP con distinto tipo,
    UNIQUE (colonia_id, zona_id)                      -- permite la llave foránea compuesta desde paquete
);

CREATE TABLE paqueteria (
    paqueteria_id  smallint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre         text     NOT NULL UNIQUE
);

-- Personas

CREATE TABLE usuario (
    usuario_id       bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_usuario   text        NOT NULL UNIQUE,
    nombre_completo  text        NOT NULL,
    hash_contrasena  text        NOT NULL,
    rol              text        NOT NULL CHECK (rol IN ('admin', 'supervisor', 'repartidor')),
    activo           boolean     NOT NULL DEFAULT true,
    creado_en        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE repartidor (
    usuario_id        bigint   PRIMARY KEY REFERENCES usuario (usuario_id),
    zona_id           smallint NOT NULL REFERENCES zona (zona_id),   -- zona habitual de su cuadrilla
    capacidad_diaria  smallint NOT NULL DEFAULT 60 CHECK (capacidad_diaria > 0)
);

-- Recepción de paquetes

CREATE TABLE manifiesto (
    manifiesto_id    bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    paqueteria_id    smallint    NOT NULL REFERENCES paqueteria (paqueteria_id),
    fecha_recepcion  date        NOT NULL,
    archivo_nombre   text        NOT NULL,
    importado_por    bigint      NOT NULL REFERENCES usuario (usuario_id),
    importado_en     timestamptz NOT NULL DEFAULT now(),
    UNIQUE (paqueteria_id, archivo_nombre)
);

-- Fragmentación horizontal: cada zona tendrá su partición.
CREATE TABLE paquete (
    paquete_id     bigint       GENERATED ALWAYS AS IDENTITY,
    zona_id        smallint     NOT NULL,
    colonia_id     integer      NOT NULL,
    manifiesto_id  bigint       NOT NULL REFERENCES manifiesto (manifiesto_id),
    guia           text         NOT NULL,
    peso_kg        numeric(6,2) CHECK (peso_kg > 0),
    estado         text         NOT NULL DEFAULT 'recibido'
                   CHECK (estado IN ('recibido', 'asignado', 'en_ruta', 'entregado', 'fallido', 'devuelto')),
    recibido_en    timestamptz  NOT NULL DEFAULT now(),
    PRIMARY KEY (zona_id, paquete_id),
    UNIQUE (zona_id, guia),
    FOREIGN KEY (colonia_id, zona_id) REFERENCES colonia (colonia_id, zona_id)
) PARTITION BY LIST (zona_id);

-- Guarda los paquetes de zonas que todavía no tienen partición propia.
CREATE TABLE paquete_sin_zona PARTITION OF paquete DEFAULT;

-- Fragmentación vertical: los datos personales del destinatario van aparte
-- para poder cifrarlos y restringirlos (issue #33). Comparte la llave del paquete.
CREATE TABLE destinatario (
    zona_id       smallint NOT NULL,
    paquete_id    bigint   NOT NULL,
    nombre        text     NOT NULL,
    telefono      text,
    calle_numero  text     NOT NULL,
    referencias   text,
    PRIMARY KEY (zona_id, paquete_id),
    FOREIGN KEY (zona_id, paquete_id) REFERENCES paquete (zona_id, paquete_id) ON DELETE CASCADE
);

-- Reparto

CREATE TABLE ruta (
    ruta_id        bigint   GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    zona_id        smallint NOT NULL REFERENCES zona (zona_id),
    repartidor_id  bigint   NOT NULL REFERENCES repartidor (usuario_id),
    fecha          date     NOT NULL,
    estado         text     NOT NULL DEFAULT 'abierta' CHECK (estado IN ('abierta', 'en_curso', 'cerrada')),
    UNIQUE (repartidor_id, fecha)
);

CREATE TABLE asignacion (
    asignacion_id  bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    zona_id        smallint    NOT NULL,
    paquete_id     bigint      NOT NULL,
    ruta_id        bigint      NOT NULL REFERENCES ruta (ruta_id),
    orden          smallint    NOT NULL CHECK (orden > 0),
    asignado_por   bigint      NOT NULL REFERENCES usuario (usuario_id),
    asignado_en    timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (zona_id, paquete_id) REFERENCES paquete (zona_id, paquete_id),
    UNIQUE (ruta_id, orden),
    UNIQUE (ruta_id, zona_id, paquete_id)
);

CREATE TABLE entrega (
    entrega_id     bigint       GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asignacion_id  bigint       NOT NULL UNIQUE REFERENCES asignacion (asignacion_id),
    resultado      text         NOT NULL CHECK (resultado IN ('entregado', 'fallido')),
    motivo_fallo   text,
    registrada_en  timestamptz  NOT NULL DEFAULT now(),
    latitud        numeric(9,6) CHECK (latitud BETWEEN -90 AND 90),
    longitud       numeric(9,6) CHECK (longitud BETWEEN -180 AND 180),
    foto_ruta      text,
    firma_ruta     text,
    CHECK (resultado = 'entregado' OR motivo_fallo IS NOT NULL)
);

-- Directorio de fragmentos: en qué partición y en qué nodo vive cada zona.

CREATE TABLE directorio_fragmentos (
    zona_id         smallint    PRIMARY KEY REFERENCES zona (zona_id),
    particion       text        NOT NULL UNIQUE,
    nodo_primario   text        NOT NULL,
    nodo_replica    text,
    actualizado_en  timestamptz NOT NULL DEFAULT now()
);