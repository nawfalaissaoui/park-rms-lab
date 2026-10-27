import pandas as pd
import pytest


@pytest.fixture(scope="session")
def small_room_types() -> pd.DataFrame:
    """Hotel pequeño para que los tests sean rápidos."""
    return pd.DataFrame(
        [(1, "Standard", 20, 140.0), (2, "Suite", 10, 320.0)],
        columns=["room_type_id", "name", "rooms_available", "base_rate"],
    )
