import time
from typing import Any, Dict, Optional, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Simple in-memory TTL cache for API responses
class _TTLCache:
	"""Minimal TTL cache keyed by a stringified params tuple."""
	def __init__(self):
		self._store: Dict[str, Any] = {}
		self._ts: Dict[str, float] = {}

	def get(self, key: str, ttl: int):
		ts = self._ts.get(key)
		if ts is None:
			return None
		if time.time() - ts > ttl:
			# expired
			self._store.pop(key, None)
			self._ts.pop(key, None)
			return None
		return self._store.get(key)

	def set(self, key: str, value: Any):
		self._store[key] = value
		self._ts[key] = time.time()

_cache = _TTLCache()

def _create_session(retries: int = 3, backoff_factor: float = 0.3, status_forcelist: tuple = (500, 502, 504)):
	"""Create a requests.Session with retry strategy."""
	s = requests.Session()
	retry = Retry(
		total=retries,
		read=retries,
		connect=retries,
		backoff_factor=backoff_factor,
		status_forcelist=status_forcelist,
		allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
	)
	adapter = HTTPAdapter(max_retries=retry)
	s.mount("https://", adapter)
	s.mount("http://", adapter)
	return s

def fetch_weather(api_url: str, params: Optional[Dict] = None, timeout: int = 10, session: Optional[requests.Session] = None, cache_ttl: int = 0):
	"""
	Récupère des données météo depuis api_url.
	Retourne le JSON décodé ou lève une exception.
	Arguments additionnels:
	- session: optional requests.Session (with retries)
	- cache_ttl: seconds to cache the response (0 = no cache)
	"""
	if session is None:
		session = _create_session()
	params = params or {}

	# cache key
	if cache_ttl and isinstance(params, dict):
		key = f"{api_url}|{'&'.join(f'{k}={params[k]}' for k in sorted(params))}"
		cached = _cache.get(key, cache_ttl)
		if cached is not None:
			return cached

	resp = session.get(api_url, params=params, timeout=timeout)
	resp.raise_for_status()
	data = resp.json()

	if cache_ttl and isinstance(params, dict):
		_cache.set(key, data)
	return data

def build_open_meteo_params(lat: float, lon: float, hourly: Optional[Sequence[str]] = None, daily: Optional[Sequence[str]] = None, timezone: str = "auto"):
	"""Return dict of query params for Open‑Meteo API."""
	params = {
		"latitude": lat,
		"longitude": lon,
		"timezone": timezone,
	}
	if hourly:
		params["hourly"] = ",".join(hourly)
	if daily:
		params["daily"] = ",".join(daily)
	return params

def fetch_open_meteo(lat: float, lon: float, hourly: Optional[Sequence[str]] = ("temperature_2m",), daily: Optional[Sequence[str]] = None, timeout: int = 10, session: Optional[requests.Session] = None, cache_ttl: int = 300):
	"""
	Convenience wrapper for Open‑Meteo (https://open-meteo.com/).
	Returns parsed JSON.
	"""
	base = "https://api.open-meteo.com/v1/forecast"
	if session is None:
		session = _create_session()
	params = build_open_meteo_params(lat, lon, hourly=hourly, daily=daily)
	# cache key
	key = f"open-meteo|{lat}|{lon}|{','.join(hourly) if hourly else ''}|{','.join(daily) if daily else ''}"
	if cache_ttl:
		cached = _cache.get(key, cache_ttl)
		if cached is not None:
			return cached

	resp = session.get(base, params=params, timeout=timeout)
	resp.raise_for_status()
	data = resp.json()

	if cache_ttl:
		_cache.set(key, data)
	return data
