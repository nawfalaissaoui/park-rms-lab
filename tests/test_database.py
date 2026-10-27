import sqlite3

import pytest

from parkrms.build_db import build_database
from parkrms.db import init_db

TABLES = {"dim_date", "dim_room_type", "fact_booking", "fact_comp_rate"}


def test_schema_creates_tables(tmp_path):
    conn = init_db(tmp_path / "t.db")
    names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert TABLES <= names


def test_foreign_keys_are_enforced(tmp_path):
    conn = init_db(tmp_path / "t.db")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO fact_booking (booking_date, stay_date, room_type_id, channel, rate, status) "
            "VALUES ('2025-01-01', '2025-02-01', 99, 'ota', 100, 'confirmed')"
        )


def test_booking_cannot_be_after_stay(tmp_path):
    conn = init_db(tmp_path / "t.db")
    conn.execute("INSERT INTO dim_room_type VALUES (1, 'Standard', 10, 100)")
    conn.execute(
        "INSERT INTO dim_date VALUES ('2025-02-01', 2025, 2, 1, 5, 1, 0, NULL, 0, 'low')"
    )
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO fact_booking (booking_date, stay_date, room_type_id, channel, rate, status) "
            "VALUES ('2025-03-01', '2025-02-01', 1, 'ota', 100, 'confirmed')"
        )


def test_build_database_end_to_end(tmp_path, small_room_types):
    db = tmp_path / "park.db"
    counts = build_database(
        str(db), start="2025-07-01", end="2025-07-31", seed=1, room_types=small_room_types
    )
    assert counts["dim_date"] == 31
    assert counts["dim_room_type"] == 2
    assert counts["fact_booking"] > 0

    conn = sqlite3.connect(db)
    n = conn.execute("SELECT COUNT(*) FROM fact_booking").fetchone()[0]
    assert n == counts["fact_booking"]
    # Ninguna habitación sobrepasa la capacidad en la base de datos.
    over = conn.execute(
        """
        SELECT COUNT(*) FROM (
            SELECT b.stay_date, b.room_type_id, COUNT(*) AS n, r.rooms_available AS cap
            FROM fact_booking b JOIN dim_room_type r USING (room_type_id)
            WHERE b.status = 'confirmed'
            GROUP BY b.stay_date, b.room_type_id
            HAVING n > cap
        )
        """
    ).fetchone()[0]
    assert over == 0
