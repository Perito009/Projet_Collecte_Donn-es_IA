# data_cleaning.py
import pandas as pd
import numpy as np


# ---------------------------------------------------------
# 1. Détection d'anomalies (outliers)
# ---------------------------------------------------------

def detect_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des colonnes 'wind_anomaly' et 'temp_anomaly'
    pour repérer les valeurs aberrantes.
    """

    # Création des colonnes par défaut
    df["wind_anomaly"] = False
    df["temp_anomaly"] = False

    # --- Détection anomalies vent ---
    # km/h > 150
    if "wind_speed" in df.columns:
        df.loc[df["wind_speed"] > 150, "wind_anomaly"] = True

    # m/s > 41.67
    if "wind_speed_ms" in df.columns:
        df.loc[df["wind_speed_ms"] > 41.67, "wind_anomaly"] = True

    # --- Détection anomalies température ---
    if "temperature" in df.columns:
        df.loc[(df["temperature"] < -80) | (df["temperature"] > 60), "temp_anomaly"] = True

    # si tu veux détecter plus (humidité, pression, etc.), je peux l’ajouter

    return df


# ---------------------------------------------------------
# 2. Nettoyage & correction des anomalies
# ---------------------------------------------------------

def clean_data(df: pd.DataFrame, drop_anomalies: bool = False) -> pd.DataFrame:
    """
    Corrige les valeurs aberrantes en remplaçant par la médiane.
    Option : supprimer totalement les lignes anormales.
    """

    # S'assurer que les colonnes d'anomalies existent
    if "wind_anomaly" not in df.columns or "temp_anomaly" not in df.columns:
        df = detect_outliers(df)

    # --- Correction vent (km/h) ---
    if "wind_speed" in df.columns and df["wind_anomaly"].any():
        median_wind = df["wind_speed"].median()
        df.loc[df["wind_anomaly"], "wind_speed"] = median_wind

    # --- Correction vent (m/s) ---
    if "wind_speed_ms" in df.columns and df["wind_anomaly"].any():
        median_wind_ms = df["wind_speed_ms"].median()
        df.loc[df["wind_anomaly"], "wind_speed_ms"] = median_wind_ms

    # --- Correction température ---
    if "temperature" in df.columns and df["temp_anomaly"].any():
        median_temp = df["temperature"].median()
        df.loc[df["temp_anomaly"], "temperature"] = median_temp

    # --- Option : suppression lignes anormales ---
    if drop_anomalies:
        df = df[(df["wind_anomaly"] == False) & (df["temp_anomaly"] == False)].reset_index(drop=True)

    return df


# ---------------------------------------------------------
# 3. TEST LOCAL — exécuté uniquement si tu fais :
#     python data_cleaning.py
# ---------------------------------------------------------

if __name__ == "__main__":
    df = pd.DataFrame({
        "wind_speed": [20, 200, 10],     # 200 km/h = aberrant
        "wind_speed_ms": [5, 60, 3],     # 60 m/s = aberrant
        "temperature": [10, -100, 30]    # -100°C = aberrant
    })

    print("=== Avant nettoyage ===")
    print(df)

    # Détection
    df = detect_outliers(df)
    print("\n=== Après détection d'anomalies ===")
    print(df)

    # Nettoyage
    df = clean_data(df)
    print("\n=== Après correction ===")
    print(df)
