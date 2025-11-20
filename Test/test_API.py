import os
import sys
import argparse
import json

# Ensure repo root is on sys.path so we can import Extract.extract_api
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
	sys.path.insert(0, repo_root)

from Extract.extract_api import fetch_open_meteo, fetch_weather

def main(argv=None):
	parser = argparse.ArgumentParser(description="Test simple des fonctions d'extraction météo")
	parser.add_argument("--mode", choices=("open-meteo", "url"), default="open-meteo",
						help="Mode de test: 'open-meteo' (par défaut) ou 'url' pour tester fetch_weather")
	parser.add_argument("--lat", type=float, default=48.8566, help="Latitude pour open-meteo (default Paris)")
	parser.add_argument("--lon", type=float, default=2.3522, help="Longitude pour open-meteo (default Paris)")
	parser.add_argument("--url", type=str, help="URL à appeler pour fetch_weather (mode 'url')")
	# parse provided argv (None -> use sys.argv[1:])
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
			print("Réponse reçue (top-level keys):", keys[:10])
			try:
				preview = json.dumps({k: data[k] for k in keys[:3]}, ensure_ascii=False, indent=2)
				print("Aperçu:", preview)
			except Exception:
				print("Aperçu indisponible (données non sérialisables).")
		else:
			print("Réponse non-dictionnaire reçue:", type(data), str(data)[:200])

		print("API test OK")
		return 0
	except Exception as exc:
		print("API test échoué:", exc, file=sys.stderr)
		return 2

if __name__ == "__main__":
	import sys as _sys
	_sys.exit(main())
