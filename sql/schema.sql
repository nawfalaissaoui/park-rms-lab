-- Esquema de park-rms-lab (SQLite).
-- Decisión de diseño: la tabla de hechos tiene grano "noche-habitación":
-- una fila = una habitación reservada para UNA noche concreta (stay_date).
-- Así el pick-up (reservas acumuladas por fecha de estancia y por antelación)
-- sale con un simple GROUP BY. Las consecuencias de esta simplificación
-- (estancias de varias noches, tarifas distintas por noche) se discuten
-- en docs/decisiones.md.
--
-- Nota: SQLite no aplica las claves foráneas a menos que cada conexión
-- ejecute PRAGMA foreign_keys = ON (lo hace parkrms.db.init_db).

CREATE TABLE IF NOT EXISTS dim_date (
    date            TEXT PRIMARY KEY,                       -- ISO AAAA-MM-DD
    year            INTEGER NOT NULL,
    month           INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    day             INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    dow             INTEGER NOT NULL CHECK (dow BETWEEN 0 AND 6),  -- 0 = lunes
    is_weekend      INTEGER NOT NULL CHECK (is_weekend IN (0, 1)),
    is_holiday      INTEGER NOT NULL CHECK (is_holiday IN (0, 1)),
    holiday_name    TEXT,
    is_school_break INTEGER NOT NULL CHECK (is_school_break IN (0, 1)),
    season          TEXT NOT NULL CHECK (season IN ('low', 'mid', 'high'))
);

CREATE TABLE IF NOT EXISTS dim_room_type (
    room_type_id    INTEGER PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    rooms_available INTEGER NOT NULL CHECK (rooms_available > 0),
    base_rate       REAL NOT NULL CHECK (base_rate > 0)
);

CREATE TABLE IF NOT EXISTS fact_booking (
    booking_id      INTEGER PRIMARY KEY,
    booking_date    TEXT NOT NULL,                          -- cuándo se reservó
    stay_date       TEXT NOT NULL REFERENCES dim_date (date),  -- noche de la estancia
    room_type_id    INTEGER NOT NULL REFERENCES dim_room_type (room_type_id),
    channel         TEXT NOT NULL CHECK (channel IN ('direct', 'ota', 'tour_operator')),
    rate            REAL NOT NULL CHECK (rate > 0),         -- EUR por noche
    status          TEXT NOT NULL CHECK (status IN ('confirmed', 'cancelled')),
    CHECK (booking_date <= stay_date)
);

CREATE INDEX IF NOT EXISTS idx_booking_stay ON fact_booking (stay_date, room_type_id);
CREATE INDEX IF NOT EXISTS idx_booking_booked ON fact_booking (booking_date);

-- Reto opcional (fase 2): precios de la competencia observados por un
-- "rate shopper" simulado.
CREATE TABLE IF NOT EXISTS fact_comp_rate (
    observed_date   TEXT NOT NULL,                          -- día en que se consultó
    stay_date       TEXT NOT NULL REFERENCES dim_date (date),
    competitor      TEXT NOT NULL,
    rate            REAL NOT NULL CHECK (rate > 0),
    PRIMARY KEY (observed_date, stay_date, competitor)
);
