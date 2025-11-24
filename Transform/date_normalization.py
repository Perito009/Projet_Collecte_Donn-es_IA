# date_normalization.py
from datetime import datetime
import pandas as pd
import pytz

def normalize_timestamp_column(df: pd.DataFrame, column: str = "ts_utc") -> pd.DataFrame:
    df[column] = pd.to_datetime(df[column], errors="coerce")

    paris_tz = pytz.timezone("Europe/Paris")
    df[column] = df[column].dt.tz_convert(paris_tz)

    df[column] = df[column].dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    return df


# -------- TEST LOCAL SI TU LANCES python date_normalization.py ----------
if __name__ == "__main__":
    df = pd.DataFrame({
        "ts_utc": [
            "2025-01-01T12:00:00Z",
            "2025-01-01 15:30:00+00:00"
        ]
    })

    print("=== Avant normalisation ===")
    print(df)

    df = normalize_timestamp_column(df, "ts_utc")

    print("\n=== Après normalisation ===")
    print(df)
