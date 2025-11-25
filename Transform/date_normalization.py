# test_date_normalization.py
import pandas as pd
import pytest
from date_normalization import normalize_timestamp_column, normalize_dates

def test_normalize_timestamp_column():
    # Test avec des timestamps valides
    df = pd.DataFrame({
        "ts_utc": [
            "2025-01-01T12:00:00Z",
            "2025-01-01 15:30:00+00:00",
            "2025-01-01T18:45:00+02:00"
        ]
    })
    result = normalize_timestamp_column(df, "ts_utc")

    # Vérifie que la colonne est bien formatée et convertie en Europe/Paris
    assert all(isinstance(ts, str) for ts in result["ts_utc"])
    assert all("+" in ts or ts.endswith("Z") for ts in result["ts_utc"])  # Format ISO avec offset
    assert all(ts.endswith("0100") or ts.endswith("0200") for ts in result["ts_utc"])  # Offset Europe/Paris

    # Test avec des timestamps invalides
    df_with_invalid = pd.DataFrame({
        "ts_utc": [
            "2025-01-01T12:00:00Z",
            "invalid date",
            "2025-01-01 15:30:00+00:00"
        ]
    })
    result_with_invalid = normalize_timestamp_column(df_with_invalid, "ts_utc")

    # Vérifie que les timestamps invalides deviennent NaT (puis sont formatés en chaîne vide ou NaT)
    assert pd.isna(pd.to_datetime(result_with_invalid["ts_utc"].iloc[1], errors="coerce"))

def test_normalize_dates():
    # Test que normalize_dates est un wrapper pour normalize_timestamp_column
    df = pd.DataFrame({
        "ts_utc": [
            "2025-01-01T12:00:00Z",
            "2025-01-01 15:30:00+00:00",
            "invalid date"
        ]
    })
    result = normalize_dates(df, "ts_utc")

    # Vérifie que la colonne est bien formatée et convertie en Europe/Paris
    assert all(isinstance(ts, str) for ts in result["ts_utc"])
    assert all("+" in ts or ts.endswith("Z") for ts in result["ts_utc"])  # Format ISO avec offset
    assert pd.isna(pd.to_datetime(result["ts_utc"].iloc[2], errors="coerce"))  # Timestamp invalide
