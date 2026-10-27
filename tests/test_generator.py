import numpy as np
import pandas as pd
import pytest

from parkrms import config
from parkrms.calendar import build_calendar
from parkrms.generator import expected_occupancy, generate_bookings

COLUMNS = [
    "booking_id", "booking_date", "stay_date", "room_type_id",
    "channel", "rate", "status",
]


@pytest.fixture(scope="module")
def cal() -> pd.DataFrame:
    return build_calendar("2025-01-01", "2025-12-31")


@pytest.fixture(scope="module")
def bookings(cal, small_room_types) -> pd.DataFrame:
    return generate_bookings(cal, small_room_types, seed=7)


# ---------- expected_occupancy ----------

def test_expected_occupancy_range_and_index(cal):
    occ = expected_occupancy(cal, np.random.default_rng(1))
    assert len(occ) == len(cal)
    assert (occ.index == cal["date"]).all()
    assert occ.between(0.10, 1.0).all()


def test_expected_occupancy_seasonality(cal):
    occ = expected_occupancy(cal, np.random.default_rng(1))
    by_month = occ.groupby(occ.index.month).mean()
    assert by_month[8] > by_month[1] + 0.25


# ---------- generate_bookings ----------

def test_columns_and_types(bookings):
    assert list(bookings.columns) == COLUMNS
    assert pd.api.types.is_datetime64_any_dtype(bookings["booking_date"])
    assert pd.api.types.is_datetime64_any_dtype(bookings["stay_date"])
    assert bookings["booking_id"].is_unique
    assert set(bookings["channel"].unique()) <= set(config.CHANNEL_MIX)
    assert set(bookings["status"].unique()) == {"confirmed", "cancelled"}
    assert (bookings["rate"] > 0).all()


def test_reproducible_with_same_seed(cal, small_room_types):
    a = generate_bookings(cal, small_room_types, seed=3)
    b = generate_bookings(cal, small_room_types, seed=3)
    c = generate_bookings(cal, small_room_types, seed=4)
    pd.testing.assert_frame_equal(a, b)
    assert not a.equals(c)


def test_lead_time_within_bounds(bookings):
    lead = (bookings["stay_date"] - bookings["booking_date"]).dt.days
    assert lead.min() >= 0
    assert lead.max() <= config.MAX_LEAD_DAYS


def test_never_exceeds_capacity(bookings, small_room_types):
    conf = bookings[bookings["status"] == "confirmed"]
    per_day = conf.groupby(["stay_date", "room_type_id"]).size().rename("n").reset_index()
    cap = small_room_types.set_index("room_type_id")["rooms_available"]
    assert (per_day["n"] <= per_day["room_type_id"].map(cap)).all()


def test_cancellation_share_near_target(bookings):
    share = (bookings["status"] == "cancelled").mean()
    assert abs(share - config.CANCELLATION_RATE) < 0.04


def test_demand_is_seasonal(bookings, small_room_types):
    conf = bookings[bookings["status"] == "confirmed"]
    total_rooms = small_room_types["rooms_available"].sum()
    daily = conf.groupby("stay_date").size() / total_rooms
    assert daily[daily.index.month == 8].mean() > daily[daily.index.month == 1].mean() + 0.25


def test_weekends_are_busier(bookings, small_room_types):
    conf = bookings[bookings["status"] == "confirmed"]
    total_rooms = small_room_types["rooms_available"].sum()
    daily = (conf.groupby("stay_date").size() / total_rooms).reindex(
        pd.date_range("2025-01-01", "2025-12-31"), fill_value=0
    )
    weekend = daily[daily.index.dayofweek >= 5].mean()
    weekday = daily[daily.index.dayofweek < 5].mean()
    assert weekend > weekday


def test_rates_higher_in_peak_season(bookings):
    conf = bookings[bookings["status"] == "confirmed"]
    month = conf["stay_date"].dt.month
    assert conf.loc[month == 8, "rate"].mean() > conf.loc[month == 1, "rate"].mean()


def test_stay_dates_inside_calendar(bookings, cal):
    assert bookings["stay_date"].min() >= cal["date"].min()
    assert bookings["stay_date"].max() <= cal["date"].max()
