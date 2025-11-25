import pandas as pd

def celsius_to_kelvin(c):
    return c + 273.15 if pd.notnull(c) else None

def kmh_to_ms(v):
    return v / 3.6 if pd.notnull(v) else None

def normalize_units(df: pd.DataFrame) -> pd.DataFrame:
    if "temperature" in df.columns:
        df["temperature_K"] = df["temperature"].apply(celsius_to_kelvin)
    if "wind_speed" in df.columns:
        df["wind_speed_ms"] = df["wind_speed"].apply(kmh_to_ms)
    return df

def convert_units(df: pd.DataFrame) -> pd.DataFrame:
    return normalize_units(df)
