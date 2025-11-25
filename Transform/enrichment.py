# test_enrichment.py
import pandas as pd
import pytest
from enrichment import (
    normalize_wind_direction,
    generate_unique_id,
    add_turbine_id,
    enrich_dataframe,
    enrich_data,
    WIND_DIRECTIONS,
)

def test_normalize_wind_direction():
    # Test avec des directions connues
    assert normalize_wind_direction("N") == "North"
    assert normalize_wind_direction("S") == "South"
    assert normalize_wind_direction("NE") == "Northeast"
    assert normalize_wind_direction("SW") == "Southwest"

    # Test avec des directions en minuscules
    assert normalize_wind_direction("ne") == "Northeast"
    assert normalize_wind_direction(" s ") == "South"

    # Test avec une direction inconnue
    assert normalize_wind_direction("XYZ") == "XYZ"

    # Test avec une valeur nulle
    assert normalize_wind_direction(None) is None
    assert pd.isna(normalize_wind_direction(pd.NA))

def test_generate_unique_id():
    # Test avec un dictionnaire contenant les clés attendues
    row = {"ts_utc": "2025-01-01T12:00:00Z", "station_id": 1}
    unique_id = generate_unique_id(row)
    assert len(unique_id) == 32  # MD5 produit un hash de 32 caractères

    # Test avec une clé manquante
    row_missing = {"ts_utc": "2025-01-01T12:00:00Z"}
    unique_id_missing = generate_unique_id(row_missing)
    assert len(unique_id_missing) == 32

def test_add_turbine_id():
    # Test avec un DataFrame contenant 'station_id'
    df = pd.DataFrame({"station_id": [1, 2, 3]})
    result = add_turbine_id(df)
    assert "turbine_id" in result.columns
    assert result["turbine_id"].tolist() == [1, 2, 3]

    # Test avec un DataFrame sans 'station_id'
    df_no_id = pd.DataFrame({"other_col": [1, 2, 3]})
    result_no_id = add_turbine_id(df_no_id)
    assert "turbine_id" in result_no_id.columns
    assert result_no_id["turbine_id"].tolist() == [1, 2, 3]  # fallback

def test_enrich_dataframe():
    # Test avec un DataFrame contenant toutes les colonnes attendues
    df = pd.DataFrame({
        "ts_utc": ["2025-01-01T12:00:00Z", "2025-01-01T14:00:00Z"],
        "station_id": [1, 2],
        "wind_direction": ["NE", "s"]
    })
    result = enrich_dataframe(df)
    assert "wind_direction_full" in result.columns
    assert "turbine_id" in result.columns
    assert "unique_id" in result.columns
    assert result["wind_direction_full"].tolist() == ["Northeast", "South"]
    assert result["turbine_id"].tolist() == [1, 2]
    assert len(result["unique_id"].iloc[0]) == 32

    # Test avec un DataFrame contenant des valeurs nulles
    df_with_nan = pd.DataFrame({
        "ts_utc": ["2025-01-01T12:00:00Z", None],
        "station_id": [1, None],
        "wind_direction": ["NE", None]
    })
    result_with_nan = enrich_dataframe(df_with_nan)
    assert pd.isna(result_with_nan["wind_direction_full"].iloc[1])
    assert result_with_nan["turbine_id"].tolist() == [1, 2]  # fallback
    assert len(result_with_nan["unique_id"].iloc[0]) == 32

def test_enrich_data():
    # Test que la fonction enrich_data est un wrapper pour enrich_dataframe
    df = pd.DataFrame({
        "ts_utc": ["2025-01-01T12:00:00Z", "2025-01-01T14:00:00Z"],
        "station_id": [1, 2],
        "wind_direction": ["NE", "s"]
    })
    result = enrich_data(df)
    assert "wind_direction_full" in result.columns
    assert "turbine_id" in result.columns
    assert "unique_id" in result.columns
    assert result["wind_direction_full"].tolist() == ["Northeast", "South"]
    assert result["turbine_id"].tolist() == [1, 2]
    assert len(result["unique_id"].iloc[0]) == 32
