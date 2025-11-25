from dotenv import load_dotenv
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

# Charger les variables d'environnement
env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    )
)

# Calculer la date et l'heure d'il y a 24 heures
yesterday = datetime.now() - timedelta(hours=24)

# Récupérer les mesures des dernières 24 heures
response = (
    supabase.table("raw_measurements")
    .select("*")
    .gt("ts_utc", yesterday.isoformat())
    .execute()
)

if response.data:
    # Créer un DataFrame à partir des données
    df = pd.DataFrame(response.data)
    print("Data successfully stored in DataFrame")
else:
    print("No data found for the last 24 hours.")
