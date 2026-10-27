"""Calendario de fechas con festivos, vacaciones escolares y temporada.

TODO fase 1.1 (tuyo): implementa `build_calendar`.
Los tests de tests/test_calendar.py definen cuándo está bien hecho.
"""
from __future__ import annotations

import pandas as pd

from parkrms import config


def build_calendar(start: str, end: str) -> pd.DataFrame:
    """Devuelve una fila por día entre `start` y `end` (ambos incluidos).

    Columnas obligatorias (coinciden con la tabla dim_date de sql/schema.sql):
        date             datetime64[ns]
        year, month, day int
        dow              int, 0 = lunes ... 6 = domingo
        is_weekend       0/1  (sábado o domingo)
        is_holiday       0/1  (festivo en España / Cataluña)
        holiday_name     str o None
        is_school_break  0/1  (según config.SCHOOL_BREAKS)
        season           'low' | 'mid' | 'high'

    Pistas:
        - pd.date_range(start, end, freq="D")
        - holidays.country_holidays(config.HOLIDAY_COUNTRY,
              subdiv=config.HOLIDAY_SUBDIV, years=range(...)) se comporta como
              un diccionario {fecha: nombre}.
        - Para las vacaciones escolares: recorre config.SCHOOL_BREAKS y marca
          los días dentro de cada intervalo.
        - `season` es decisión tuya (por ejemplo, a partir de
          config.MONTHLY_BASE_OCCUPANCY). Documenta tu regla en
          docs/decisiones.md: te la preguntarán en la entrevista.
    """
    raise NotImplementedError("TODO fase 1.1: construir el calendario")
