import time
import json
import requests
from pathlib import Path
import pandas as pd
from datetime import datetime

class TTLCache:
    """Simple in-memory TTL cache for API responses."""
    def __init__(self):
        self._store = {}
        self._ts = {}

    def get(self, key: str, ttl: int) -> any:
        ts = self._ts.get(key)
        if ts is None or time.time() - ts > ttl:
            self._store.pop(key, None)
            self._ts.pop(key, None)
            return None
        return self._store.get(key)

    def set(self, key: str, value: any) -> None:
        self._store[key] = value
        self._ts[key] = time.time()

_cache = TTLCache()

def create_session() -> requests.Session:
    """Create a requests.Session with retry strategy."""
    session = requests.Session()
    retry = requests.packages.urllib3.util.retry.Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_open_meteo(lat: float, lon: float) -> any:
    """
    Fetch weather data from Open-Meteo API.
    Returns parsed JSON with temperature, wind speed, humidity, and pressure.
    """
    base = "https://api.open-meteo.com/v1/forecast"
    session = create_session()
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m,pressure_msl",
        "timezone": "auto"
    }
    response = session.get(base, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def extract_data_to_dataframe(lat: float = 48.8566, lon: float = 2.3522) -> pd.DataFrame:
    """
    Extract weather data from Open-Meteo API and store it in a DataFrame.
    Save the data to a JSON file in the 'energitic-pipeline' directory.
    """
    data = fetch_open_meteo(lat, lon)

    # Extract relevant variables
    hourly_data = data.get("hourly", {})
    relevant_vars = {
        "timestamp": hourly_data.get("time", []),
        "temperature": hourly_data.get("temperature_2m", []),
        "humidity": hourly_data.get("relativehumidity_2m", []),
        "wind_speed": hourly_data.get("windspeed_10m", []),
        "pressure": hourly_data.get("pressure_msl", [])
    }

    # Create DataFrame
    df = pd.DataFrame(relevant_vars)

    # Convert timestamp to datetime
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Save the data to a JSON file
    output_dir = Path(__file__).parent / "energitic_pipeline"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"weather_data_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"

    with open(output_file, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    print(f"Data successfully saved to {output_file}")
    return df

if __name__ == "__main__":
    df = extract_data_to_dataframe()
    print("\nData successfully stored in DataFrame")
    print(df.head())
