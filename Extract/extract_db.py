from dotenv import load_dotenv
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import csv

def init_supabase_client() -> Client:
    """
    Initialise et retourne un client Supabase en chargeant les variables d'environnement.

    Returns:
        Client: Une instance du client Supabase configurée.
    """
    env_path = Path(__file__).with_name(".env")
    load_dotenv(env_path)

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("Les variables d'environnement SUPABASE_URL et SUPABASE_KEY doivent être définies.")

    supabase: Client = create_client(
        url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
            schema="public",
        )
    )

    return supabase

def extract_data_to_dataframe():
    # Initialiser le client Supabase
    supabase = init_supabase_client()

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
        # Spécifier le répertoire et le nom du fichier
        output_dir = Path(__file__).parent / "energitic_pipeline"
        output_file = output_dir / "measurements_last_24hours.csv"

        # Créer le répertoire s'il n'existe pas
        output_dir.mkdir(exist_ok=True)

        # Écrire les données dans un fichier CSV
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Écrire l'en-tête
            writer.writerow(response.data[0].keys())
            # Écrire les données
            for row in response.data:
                writer.writerow(row.values())

        print(f"Data successfully saved to {output_file}")

        # Créer un DataFrame à partir des données
        df = pd.DataFrame(response.data)
        print("Data successfully stored in DataFrame")
        return df
    else:
        print("No data found for the last 24 hours.")
        return pd.DataFrame()  # Retourne un DataFrame vide si aucune donnée n'est trouvée
