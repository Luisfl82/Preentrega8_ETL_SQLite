# Preentrega 8 - Persistencia e integración de scripts ETL

Script que **extrae** ventas de un CSV, las **transforma** (limpieza + columna `total_venta`) y las **carga** en una base de datos local **SQLite**.

## Requisitos
- Python 3.9+
- Librerías: `pandas`, `numpy` (SQLite ya viene incluido en Python)

## Pasos para ejecutar
1. `pip install -r requirements.txt`
2. `python generar_datos.py` (crea `data/ventas_origen.csv`)
3. `python etl_sqlite.py`
4. Se crea `ventas.db` con la tabla `ventas_resumen`.

## Patrón de datos
ETL por lotes (batch): origen CSV → transformación en pandas → tabla destino en SQLite, definida en `esquema.sql` (DDL).

## Evita duplicados
La tabla se crea con `CREATE TABLE IF NOT EXISTS`, tiene clave primaria `id_venta` y antes de cargar se hace un `DELETE`, por lo que ejecutar el script varias veces deja siempre el mismo resultado.

## Manejo de errores
Controla archivo de origen inexistente y errores de la base de datos, con mensajes claros.
