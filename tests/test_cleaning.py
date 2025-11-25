# test_data_cleaning.py
import pandas as pd
import pytest
from Transform.data_cleaning import detect_outliers, clean_data


def test_detect_outliers():
    # DataFrame avec des valeurs normales et aberrantes
    df = pd.DataFrame({
        "wind_speed": [20, 200, 10],
        "wind_speed_ms": [5, 60, 3],
        "temperature": [10, -100, 30]
    })
    result = detect_outliers(df)

    # Vérifie que les colonnes d'anomalies sont ajoutées
    assert "wind_anomaly" in result.columns
    assert "temp_anomaly" in result.columns

    # Vérifie que les anomalies sont détectées
    assert result["wind_anomaly"].tolist() == [False, True, False]
    assert result["temp_anomaly"].tolist() == [False, True, False]

    # Test avec un DataFrame sans anomalies
    df_no_anomalies = pd.DataFrame({
        "wind_speed": [20, 30, 10],
        "temperature": [10, 20, 30]
    })
    result_no_anomalies = detect_outliers(df_no_anomalies)
    assert result_no_anomalies["wind_anomaly"].sum() == 0
    assert result_no_anomalies["temp_anomaly"].sum() == 0

def test_clean_data_without_drop():
    # DataFrame avec des valeurs normales et aberrantes
    df = pd.DataFrame({
        "wind_speed": [20, 200, 10],
        "wind_speed_ms": [5, 60, 3],
        "temperature": [10, -100, 30]
    })
    result = clean_data(df, drop_anomalies=False)

    # Vérifie que les anomalies sont corrigées par la médiane
    median_wind = df["wind_speed"].median()
    median_wind_ms = df["wind_speed_ms"].median()
    median_temp = df["temperature"].median()

    assert result.loc[1, "wind_speed"] == median_wind
    assert result.loc[1, "wind_speed_ms"] == median_wind_ms
    assert result.loc[1, "temperature"] == median_temp

def test_clean_data_with_drop():
    # DataFrame avec des valeurs normales et aberrantes
    df = pd.DataFrame({
        "wind_speed": [20, 200, 10],
        "wind_speed_ms": [5, 60, 3],
        "temperature": [10, -100, 30]
    })
    result = clean_data(df, drop_anomalies=True)

    # Vérifie que les lignes avec anomalies sont supprimées
    assert len(result) == 2
    assert result["wind_anomaly"].sum() == 0
    assert result["temp_anomaly"].sum() == 0

def test_clean_data_without_anomalies():
    # DataFrame sans anomalies
    df = pd.DataFrame({
        "wind_speed": [20, 30, 10],
        "temperature": [10, 20, 30]
    })
    result = clean_data(df, drop_anomalies=False)

    # Vérifie que rien n'est modifié
    assert result.equals(df)
