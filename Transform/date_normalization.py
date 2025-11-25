# date_normalization.py
from datetime import datetime
import pandas as pd
import pytz
from typing import Optional

def normalize_timestamp_column(df: pd.DataFrame, column: str = "ts_utc") -> pd.DataFrame:
    """
    Compatibilité historique : convertit une colonne de timestamps en format
    ISO localisé (Europe/Paris).
    """
    # Parse en UTC si possible, gérer les erreurs en produisant NaT
    series = pd.to_datetime(df[column], errors="coerce", utc=True)

    # Convertir en timezone Europe/Paris
    paris_tz = pytz.timezone("Europe/Paris")
    series = series.dt.tz_convert(paris_tz)

    # Format ISO sans séparateur ':' dans l'offset pour compatibilité simple
    df[column] = series.dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    return df

def normalize_dates(df: pd.DataFrame, column: str = "ts_utc") -> pd.DataFrame:
    """
    API attendue par run_transform.py — wrapper clair vers normalize_timestamp_column.
    """
    return normalize_timestamp_column(df, column=column)


# -------- TEST LOCAL SI TU LANCES python date_normalization.py ----------
if __name__ == "__main__":
    df = pd.DataFrame({
        "ts_utc": [
            "2025-01-01T12:00:00Z",
            "2025-01-01 15:30:00+00:00",
            "invalid date"
        ]
    })

    print("=== Avant normalisation ===")
    print(df)

    df = normalize_dates(df, "ts_utc")

    print("\n=== Après normalisation ===")
    print(df)
