"""Generador de reservas sintéticas.

TODO fase 1.2 y 1.3 (tuyo): implementa `expected_occupancy` y `generate_bookings`.
Antes de programar, lee docs/conceptos.md (ocupación, ADR, lead time, cancelaciones).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from parkrms import config


def default_room_types() -> pd.DataFrame:
    """Tipos de habitación de config.ROOM_TYPES como DataFrame (ya hecho)."""
    return pd.DataFrame(
        config.ROOM_TYPES,
        columns=["room_type_id", "name", "rooms_available", "base_rate"],
    )


def expected_occupancy(cal: pd.DataFrame, rng: np.random.Generator) -> pd.Series:
    """Ocupación esperada (fracción entre 0.10 y 1.0) para cada día del calendario.

    Devuelve una Series indexada por `cal["date"]`.

    Idea: parte de config.MONTHLY_BASE_OCCUPANCY[mes], suma los bonus de fin de
    semana, festivo y vacaciones escolares, añade ruido normal
    (config.NOISE_STD) y limita el resultado a [0.10, 1.0].

    Pregunta para ti: ¿por qué el ruido lo generamos con un `rng` recibido por
    parámetro y no con np.random.* a pelo? (Pista: reproducibilidad.)
    """
    raise NotImplementedError("TODO fase 1.2: ocupación esperada por día")


def generate_bookings(
    cal: pd.DataFrame,
    room_types: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Genera reservas a grano noche-habitación (ver sql/schema.sql).

    Columnas de salida:
        booking_id    int, único (1..n)
        booking_date  datetime64[ns]  (cuándo se reservó)
        stay_date     datetime64[ns]  (noche de la estancia, dentro de `cal`)
        room_type_id  int             (de `room_types`)
        channel       'direct' | 'ota' | 'tour_operator' (config.CHANNEL_MIX)
        rate          float > 0, EUR por noche
        status        'confirmed' | 'cancelled'

    Reglas que deben cumplirse (los tests las comprueban):
        1. Reproducible: misma `seed` -> mismo resultado exacto.
        2. Por cada (stay_date, room_type) las reservas 'confirmed' no superan
           `rooms_available`.
        3. 0 <= stay_date - booking_date <= config.MAX_LEAD_DAYS días.
        4. La fracción de 'cancelled' ronda config.CANCELLATION_RATE.
        5. Más ocupación y tarifa media en agosto que en enero; más ocupación
           en fin de semana que entre semana.

    Pasos sugeridos, por tipo de habitación:
        a) n_confirmadas = round(ocupación_esperada * rooms_available) por día.
        b) n_canceladas adicionales para que cancelled/total ≈ CANCELLATION_RATE.
        c) Repite cada stay_date tantas veces como reservas tenga (np.repeat).
        d) Antelación (lead time): distribución sesgada a la derecha, por
           ejemplo lognormal con mediana config.MEDIAN_LEAD_DAYS, redondeada y
           limitada a [0, MAX_LEAD_DAYS]. booking_date = stay_date - lead.
        e) Canal: rng.choice con las probabilidades de config.CHANNEL_MIX.
        f) Tarifa: base_rate * factor que crezca con la demanda del día, con un
           poco de ruido. Decide tú el factor y explícalo en docs/decisiones.md.

    Consejo de rendimiento: evita bucles fila a fila; con numpy/pandas
    vectorizado, 3 años tardan segundos.
    """
    raise NotImplementedError("TODO fase 1.3: generar reservas")
