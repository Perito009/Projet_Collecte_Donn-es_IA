import pandas as pd
import hashlib

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
    if pd.isnull(direction):
        return None
    direction = str(direction).upper().strip()
    return WIND_DIRECTIONS.get(direction, direction)

def generate_unique_id(row):
    base = f"{row.get('ts_utc', '')}-{row.get('station_id', '')}"
    return hashlib.md5(base.encode()).hexdigest()

def add_turbine_id(df: pd.DataFrame) -> pd.DataFrame:
    if "station_id" in df.columns:
        df["turbine_id"] = df["station_id"]
    else:
        df["turbine_id"] = df.index + 1
    return df

def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if "wind_direction" in df.columns:
        df["wind_direction_full"] = df["wind_direction"].apply(normalize_wind_direction)
    df = add_turbine_id(df)
    df["unique_id"] = df.apply(generate_unique_id, axis=1)
    return df

def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    return enrich_dataframe(df)
