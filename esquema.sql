-- DDL de la tabla de destino
CREATE TABLE IF NOT EXISTS ventas_resumen (
    id_venta      INTEGER PRIMARY KEY,
    fecha         TEXT    NOT NULL,
    producto      TEXT    NOT NULL,
    cantidad      INTEGER NOT NULL,
    precio_unit   REAL    NOT NULL,
    total_venta   REAL    NOT NULL
);
