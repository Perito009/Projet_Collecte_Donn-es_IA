# enrichment.py
import pandas as pd
import hashlib


# -------------------------------
# 1. Normalisation direction vent
# -------------------------------

WIND_DIRECTIONS = {
    "N": "North",
    "S": "South",
    "E": "East",
    "W": "West",
    "NE": "Northeast",
    "NW": "Northwest",
    "SE": "Southeast",
    "SW": "Southwest",
}

def normalize_wind_direction(direction):
    """
    Convertit une direction vent brut en direction harmonisée.
    Ex: 'NE' -> 'Northeast'
    """
    if pd.isnull(direction):
        return None

    direction = str(direction).upper().strip()
    return WIND_DIRECTIONS.get(direction, direction)  # garde valeur brute si inconnue


# -------------------------------
# 2. Génération d'identifiant unique
# -------------------------------

def generate_unique_id(row):
    """
    Génère un identifiant unique basé sur timestamp + station/turbine.
    """
    base = f"{row.get('ts_utc', '')}-{row.get('station_id', '')}"
    return hashlib.md5(base.encode()).hexdigest()


# -------------------------------
# 3. Ajout d'id de turbine
# -------------------------------

def add_turbine_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute un turbine_id, basé sur station_id si présent.
    """
    if "station_id" in df.columns:
        df["turbine_id"] = df["station_id"]
    else:
        df["turbine_id"] = df.index + 1  # fallback simple

    return df


# -------------------------------
# 4. Fonction principale d'enrichissement
# -------------------------------

def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Direction du vent
    if "wind_direction" in df.columns:
        df["wind_direction_full"] = df["wind_direction"].apply(normalize_wind_direction)

    # Ajout du turbine_id
    df = add_turbine_id(df)

    # Identifiant unique
    df["unique_id"] = df.apply(generate_unique_id, axis=1)

    return df


# -------------------------------
# 5. TEST LOCAL (exécuté si tu tapes python enrichment.py)
# -------------------------------

if __name__ == "__main__":
    df = pd.DataFrame({
        "ts_utc": ["2025-01-01T12:00:00Z", "2025-01-01T14:00:00Z"],
        "station_id": [1, 2],
        "wind_direction": ["NE", "s"]
    })

    print("=== Avant enrichment ===")
    print(df)

    df = enrich_dataframe(df)

    print("\n=== Après enrichment ===")
    print(df)
