"""Preentrega 8 - ETL: CSV (origen) -> limpieza -> SQLite (destino analítico).
El proceso es REPETIBLE: se puede ejecutar muchas veces sin duplicar datos."""
import logging
import sqlite3
import sys

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

ORIGEN = "data/ventas_origen.csv"
DB = "ventas.db"
DDL = "esquema.sql"


def extraer():
    try:
        return pd.read_csv(ORIGEN)
    except FileNotFoundError:
        logging.error("No existe %s. Ejecutá primero: python generar_datos.py", ORIGEN)
        sys.exit(1)


def transformar(df):
    df = df.dropna(subset=["producto"]).drop_duplicates(subset=["id_venta"]).copy()
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")
    df["total_venta"] = df["cantidad"] * df["precio_unit"]
    return df[["id_venta", "fecha", "producto", "cantidad", "precio_unit", "total_venta"]]


def cargar(df):
    conn = None
    try:
        conn = sqlite3.connect(DB)
        with open(DDL, encoding="utf-8") as f:
            conn.executescript(f.read())          # crea la tabla si no existe (IF NOT EXISTS)
        conn.execute("DELETE FROM ventas_resumen")  # limpieza previa: evita duplicados al re-ejecutar
        df.to_sql("ventas_resumen", conn, if_exists="append", index=False)
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM ventas_resumen").fetchone()[0]
        logging.info("Carga OK. Filas en ventas_resumen: %s", total)
    except sqlite3.Error as e:
        logging.error("Error de base de datos: %s", e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    datos = extraer()
    logging.info("Extraídas %s filas", len(datos))
    limpios = transformar(datos)
    logging.info("Tras limpieza: %s filas", len(limpios))
    cargar(limpios)
