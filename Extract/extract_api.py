import requests

def fetch_weather(api_url, params=None, timeout=10):
	"""
	Récupère des données météo depuis api_url.
	Retourne le JSON décodé ou lève une exception.
	"""
	resp = requests.get(api_url, params=params, timeout=timeout)
	resp.raise_for_status()
	return resp.json()
