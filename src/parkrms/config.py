"""Parámetros del generador de datos sintéticos.

Todos los valores son SUPUESTOS del proyecto, no datos de ninguna empresa real.
Ajústalos si quieres y deja escrito el porqué en docs/decisiones.md.
"""

DEFAULT_START = "2024-01-01"
DEFAULT_END = "2026-12-31"

# Festivos: España, subdivisión Cataluña (librería `holidays`).
HOLIDAY_COUNTRY = "ES"
HOLIDAY_SUBDIV = "CT"

# (room_type_id, nombre, habitaciones disponibles, tarifa base EUR/noche)
ROOM_TYPES = [
    (1, "Standard", 250, 140.0),
    (2, "Family", 150, 190.0),
    (3, "Suite", 50, 320.0),
]

# Reparto de reservas por canal (debe sumar 1).
CHANNEL_MIX = {"direct": 0.45, "ota": 0.40, "tour_operator": 0.15}

CANCELLATION_RATE = 0.12   # fracción de reservas canceladas sobre el total
MEDIAN_LEAD_DAYS = 35      # antelación mediana de reserva
MAX_LEAD_DAYS = 270        # nadie reserva con más de 9 meses

# Ocupación esperada por mes (fracción de habitaciones) antes de ajustes.
MONTHLY_BASE_OCCUPANCY = {
    1: 0.45, 2: 0.50, 3: 0.60, 4: 0.70, 5: 0.72, 6: 0.80,
    7: 0.92, 8: 0.95, 9: 0.78, 10: 0.68, 11: 0.48, 12: 0.60,
}
WEEKEND_BONUS = 0.06
HOLIDAY_BONUS = 0.08
SCHOOL_BREAK_BONUS = 0.05
NOISE_STD = 0.04           # desviación típica del ruido diario de ocupación

# Vacaciones escolares (inclusive). APROXIMADAS: verifica las fechas con el
# calendario escolar oficial del Departament d'Educació y corrígelas.
SCHOOL_BREAKS = [
    ("2024-03-25", "2024-04-01"),  # Semana Santa 2024
    ("2024-06-22", "2024-09-10"),  # Verano 2024
    ("2024-12-21", "2025-01-07"),  # Navidad 2024-25
    ("2025-04-14", "2025-04-21"),  # Semana Santa 2025
    ("2025-06-21", "2025-09-10"),  # Verano 2025
    ("2025-12-20", "2026-01-07"),  # Navidad 2025-26
    ("2026-03-30", "2026-04-06"),  # Semana Santa 2026
    ("2026-06-20", "2026-09-10"),  # Verano 2026
    ("2026-12-19", "2027-01-07"),  # Navidad 2026-27
]
