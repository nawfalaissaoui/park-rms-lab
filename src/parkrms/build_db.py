"""Construye la base de datos SQLite completa: python -m parkrms.build_db

TODO fase 1.4 (tuyo): implementa `build_database`. El `main` ya está hecho.
"""
from __future__ import annotations

import argparse

import pandas as pd

from parkrms import config


def build_database(
    db_path: str,
    start: str = config.DEFAULT_START,
    end: str = config.DEFAULT_END,
    seed: int = 42,
    room_types: pd.DataFrame | None = None,
) -> dict[str, int]:
    """Crea la base de datos en `db_path` y la rellena.

    Pasos:
        1. build_calendar(start, end)
        2. room_types por defecto = generator.default_room_types()
        3. generate_bookings(...)
        4. db.init_db(db_path) y db.load_dataframe(...) en este orden
           (las claves foráneas exigen cargar primero las dimensiones):
           dim_date -> dim_room_type -> fact_booking.

    Devuelve {nombre_tabla: filas_insertadas} para las tres tablas.
    """
    raise NotImplementedError("TODO fase 1.4: construir la base de datos")


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera la base de datos sintética.")
    parser.add_argument("--out", default="data/parkrms.db")
    parser.add_argument("--start", default=config.DEFAULT_START)
    parser.add_argument("--end", default=config.DEFAULT_END)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    counts = build_database(args.out, args.start, args.end, args.seed)
    for table, n in counts.items():
        print(f"{table}: {n} filas")


if __name__ == "__main__":
    main()
