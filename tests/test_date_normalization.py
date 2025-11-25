from datetime import datetime
import pandas as pd
import pytz
from typing import Optional

def normalize_timestamp_column(df: pd.DataFrame, column: str = "ts_utc") -> pd.DataFrame:
    series = pd.to_datetime(df[column], errors="coerce", utc=True)
    paris_tz = pytz.timezone("Europe/Paris")
    series = series.dt.tz_convert(paris_tz)
    df[column] = series.dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    return df

def normalize_dates(df: pd.DataFrame, column: str = "ts_utc") -> pd.DataFrame:
    return normalize_timestamp_column(df, column=column)
