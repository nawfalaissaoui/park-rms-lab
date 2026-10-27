"""Utilidades de base de datos (SQLite). Esta parte ya está hecha: es fontanería."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"


def init_db(db_path: str | Path, schema_path: str | Path = SCHEMA_PATH) -> sqlite3.Connection:
    """Abre (o crea) la base de datos, activa claves foráneas y crea las tablas."""
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")  # hay que activarlo en CADA conexión
    conn.executescript(Path(schema_path).read_text(encoding="utf-8"))
    return conn


def load_dataframe(conn: sqlite3.Connection, table: str, df: pd.DataFrame) -> int:
    """Inserta un DataFrame en `table`. Convierte fechas a texto ISO (AAAA-MM-DD).

    Devuelve el número de filas insertadas. `table` debe ser un nombre de
    tabla propio, nunca texto introducido por un usuario.
    """
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_datetime64_any_dtype(out[col]):
            out[col] = out[col].dt.strftime("%Y-%m-%d")
    out.to_sql(table, conn, if_exists="append", index=False, chunksize=5000)
    conn.commit()
    return len(out)
