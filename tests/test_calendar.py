import pandas as pd
import pytest

from parkrms.calendar import build_calendar

COLUMNS = [
    "date", "year", "month", "day", "dow", "is_weekend",
    "is_holiday", "holiday_name", "is_school_break", "season",
]


@pytest.fixture(scope="module")
def cal() -> pd.DataFrame:
    return build_calendar("2024-01-01", "2025-12-31")


def row(cal: pd.DataFrame, day: str) -> pd.Series:
    return cal.loc[cal["date"] == pd.Timestamp(day)].iloc[0]


def test_one_row_per_day_inclusive(cal):
    assert len(cal) == 731  # 2024 es bisiesto: 366 + 365
    assert cal["date"].is_unique
    assert cal["date"].is_monotonic_increasing
    assert cal["date"].iloc[0] == pd.Timestamp("2024-01-01")
    assert cal["date"].iloc[-1] == pd.Timestamp("2025-12-31")


def test_required_columns(cal):
    assert list(cal.columns[: len(COLUMNS)]) == COLUMNS
    assert pd.api.types.is_datetime64_any_dtype(cal["date"])


def test_day_of_week_and_weekend(cal):
    sat = row(cal, "2025-06-14")  # sábado
    wed = row(cal, "2025-06-11")  # miércoles
    assert sat["dow"] == 5 and sat["is_weekend"] == 1
    assert wed["dow"] == 2 and wed["is_weekend"] == 0
    assert row(cal, "2025-06-15")["is_weekend"] == 1  # domingo


@pytest.mark.parametrize("day", ["2025-01-06", "2025-12-25", "2025-09-11"])
def test_holidays_flagged_with_name(cal, day):
    r = row(cal, day)
    assert r["is_holiday"] == 1
    assert isinstance(r["holiday_name"], str) and r["holiday_name"]


def test_regular_day_is_not_holiday(cal):
    r = row(cal, "2025-03-12")
    assert r["is_holiday"] == 0
    assert pd.isna(r["holiday_name"])


def test_school_breaks(cal):
    assert row(cal, "2025-08-15")["is_school_break"] == 1   # verano
    assert row(cal, "2025-04-16")["is_school_break"] == 1   # Semana Santa
    assert row(cal, "2025-10-15")["is_school_break"] == 0   # curso escolar


def test_flags_are_binary_and_season_valid(cal):
    for col in ("is_weekend", "is_holiday", "is_school_break"):
        assert set(cal[col].unique()) <= {0, 1}
    assert set(cal["season"].unique()) <= {"low", "mid", "high"}


def test_season_follows_demand(cal):
    """Agosto debe ser temporada más alta que enero (define tú la regla)."""
    order = {"low": 0, "mid": 1, "high": 2}
    aug = cal.loc[cal["month"] == 8, "season"].map(order).mean()
    jan = cal.loc[cal["month"] == 1, "season"].map(order).mean()
    assert aug > jan
