# test_unit_conversion.py
import pandas as pd
import pytest
from unit_conversion import celsius_to_kelvin, kmh_to_ms, normalize_units, convert_units

def test_celsius_to_kelvin():
    # Test avec des valeurs normales
    assert celsius_to_kelvin(20) == 293.15
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(-10) == 263.15

    # Test avec une valeur nulle (NaN)
    assert celsius_to_kelvin(None) is None
    assert celsius_to_kelvin(pd.NA) is None
    assert pd.isna(celsius_to_kelvin(pd.NA))

def test_kmh_to_ms():
    # Test avec des valeurs normales
    assert kmh_to_ms(36) == 10.0
    assert kmh_to_ms(10) == pytest.approx(2.777777778)
    assert kmh_to_ms(90) == 25.0

    # Test avec une valeur nulle (NaN)
    assert kmh_to_ms(None) is None
    assert kmh_to_ms(pd.NA) is None
    assert pd.isna(kmh_to_ms(pd.NA))

def test_normalize_units():
    # Test avec un DataFrame contenant des valeurs normales
    df = pd.DataFrame({
        "temperature": [20, 0, -10],
        "wind_speed": [36, 10, 90]
    })
    result = normalize_units(df)
    assert "temperature_K" in result.columns
    assert "wind_speed_ms" in result.columns
    assert result["temperature_K"].tolist() == [293.15, 273.15, 263.15]
    assert result["wind_speed_ms"].tolist() == [10.0, pytest.approx(2.777777778), 25.0]

    # Test avec un DataFrame contenant des valeurs nulles
    df_with_nan = pd.DataFrame({
        "temperature": [20, None, -10],
        "wind_speed": [36, pd.NA, 90]
    })
    result_with_nan = normalize_units(df_with_nan)
    assert pd.isna(result_with_nan["temperature_K"].iloc[1])
    assert pd.isna(result_with_nan["wind_speed_ms"].iloc[1])

def test_convert_units():
    # Test que la fonction convert_units est un wrapper pour normalize_units
    df = pd.DataFrame({
        "temperature": [20, 0, -10],
        "wind_speed": [36, 10, 90]
    })
    result = convert_units(df)
    assert "temperature_K" in result.columns
    assert "wind_speed_ms" in result.columns
    assert result["temperature_K"].tolist() == [293.15, 273.15, 263.15]
    assert result["wind_speed_ms"].tolist() == [10.0, pytest.approx(2.777777778), 25.0]
