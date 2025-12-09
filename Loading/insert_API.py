import json
from pathlib import Path
from Extract.extract_db import init_supabase_client  # Importer la fonction depuis extract_db.py

# -----------------------------
# Chargement du fichier JSON
# -----------------------------
json_path = Path("Extract/energitic_pipeline/weather_data_20251127T130923Z.json")
with open(json_path, "r") as f:
    data = json.load(f)

hourly = data["hourly"]
time_list = hourly["time"]
temp_list = hourly["temperature_2m"]
humidity_list = hourly["relativehumidity_2m"]
wind_list = hourly["windspeed_10m"]
pressure_list = hourly["pressure_msl"]
latitude = data["latitude"]
longitude = data["longitude"]

# -----------------------------
# Construction des lignes à insérer
# -----------------------------
rows = []
for i in range(len(time_list)):
    rows.append({
        "timestamp": time_list[i],
        "temperature_2m": temp_list[i],
        "humidity_2m": humidity_list[i],
        "windspeed_10m": wind_list[i],
        "pressure_msl": pressure_list[i],
        "latitude": latitude,
        "longitude": longitude,
    })

# -----------------------------
# Envoi vers Supabase (en batch)
# -----------------------------
supabase = init_supabase_client()  # Utiliser la fonction importée
print(f"Insertion de {len(rows)} lignes dans la table weather_hourly...")
response = supabase.table("weather_hourly").insert(rows).execute()
print("Insertion terminée !")
print(response)
