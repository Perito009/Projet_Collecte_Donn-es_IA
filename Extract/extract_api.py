import time
from typing import Any, Dict, Optional, Sequence
import argparse
import json
import sys
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class TTLCache:
    """Simple in-memory TTL cache for API responses."""
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._ts: Dict[str, float] = {}

    def get(self, key: str, ttl: int) -> Optional[Any]:
        ts = self._ts.get(key)
        if ts is None or time.time() - ts > ttl:
            self._store.pop(key, None)
            self._ts.pop(key, None)
            return None
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._ts[key] = time.time()

_cache = TTLCache()

def create_session(
    retries: int = 3,
    backoff_factor: float = 0.3,
    status_forcelist: tuple = (500, 502, 504),
) -> requests.Session:
    """Create a requests.Session with retry strategy."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_weather(
    api_url: str,
    params: Optional[Dict] = None,
    timeout: int = 10,
    session: Optional[requests.Session] = None,
    cache_ttl: int = 0,
) -> Any:
    """
    Fetch weather data from api_url.
    Returns parsed JSON or raises an exception.
    """
    session = session or create_session()
    params = params or {}

    if cache_ttl and isinstance(params, dict):
        key = f"{api_url}|{'&'.join(f'{k}={params[k]}' for k in sorted(params))}"
        cached = _cache.get(key, cache_ttl)
        if cached is not None:
            return cached

    response = session.get(api_url, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if cache_ttl and isinstance(params, dict):
        _cache.set(key, data)

    return data

def build_open_meteo_params(
    lat: float,
    lon: float,
    hourly: Optional[Sequence[str]] = None,
    daily: Optional[Sequence[str]] = None,
    timezone: str = "auto",
) -> Dict[str, str]:
    """Build query params for Open-Meteo API."""
    params = {"latitude": lat, "longitude": lon, "timezone": timezone}
    if hourly:
        params["hourly"] = ",".join(hourly)
    if daily:
        params["daily"] = ",".join(daily)
    return params

def fetch_open_meteo(
    lat: float,
    lon: float,
    hourly: Optional[Sequence[str]] = ("temperature_2m",),
    daily: Optional[Sequence[str]] = None,
    timeout: int = 10,
    session: Optional[requests.Session] = None,
    cache_ttl: int = 300,
) -> Any:
    """
    Convenience wrapper for Open-Meteo API.
    Returns parsed JSON.
    """
    base = "https://api.open-meteo.com/v1/forecast"
    session = session or create_session()
    params = build_open_meteo_params(lat, lon, hourly=hourly, daily=daily)

    key = f"open-meteo|{lat}|{lon}|{','.join(hourly) if hourly else ''}|{','.join(daily) if daily else ''}"
    if cache_ttl:
        cached = _cache.get(key, cache_ttl)
        if cached is not None:
            return cached

    response = session.get(base, params=params, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if cache_ttl:
        _cache.set(key, data)

    return data

def main(argv=None):
    """Simple test of weather extraction functions."""
    parser = argparse.ArgumentParser(description="Simple test of weather extraction functions")
    parser.add_argument(
        "--mode",
        choices=("open-meteo", "url"),
        default="open-meteo",
        help="Test mode: 'open-meteo' (default) or 'url' for fetch_weather",
    )
    parser.add_argument("--lat", type=float, default=48.8566, help="Latitude for open-meteo (default Paris)")
    parser.add_argument("--lon", type=float, default=2.3522, help="Longitude for open-meteo (default Paris)")
    parser.add_argument("--url", type=str, help="URL to call for fetch_weather (mode 'url')")

    args = parser.parse_args(argv)

    try:
        if args.mode == "open-meteo":
            print(f"Testing Open-Meteo for lat={args.lat} lon={args.lon} ...")
            data = fetch_open_meteo(args.lat, args.lon, hourly=("temperature_2m",), cache_ttl=0, timeout=10)
        else:
            if not args.url:
                parser.error("--url is required when mode='url'")
            print(f"Testing fetch_weather against {args.url} ...")
            data = fetch_weather(args.url, params=None, cache_ttl=0, timeout=10)

        if isinstance(data, dict):
            keys = list(data.keys())
            print("Response received (top-level keys):", keys[:10])
            try:
                preview = json.dumps({k: data[k] for k in keys[:3]}, ensure_ascii=False, indent=2)
                print("Preview:", preview)
            except Exception:
                print("Preview unavailable (non-serializable data).")
        else:
            print("Non-dict response received:", type(data), str(data)[:200])

        print("API OK")
        return 0

    except Exception as exc:
        print("API failed:", exc, file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
