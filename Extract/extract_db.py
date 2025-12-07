from dotenv import load_dotenv
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

def init_supabase_client() -> Client:
    """
    Initialise et retourne un client Supabase en chargeant les variables d'environnement.
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

def extract_data_to_dataframe() -> pd.DataFrame:
    """
    Récupère les mesures des dernières 24 heures depuis Supabase et les retourne sous forme de DataFrame.
    """
    supabase = init_supabase_client()
    yesterday = datetime.now() - timedelta(hours=24)

    response = (
        supabase.table("raw_measurements")
        .select("*")
        .gt("ts_utc", yesterday.isoformat())
        .execute()
    )

    if not response.data:
        print("No data found for the last 24 hours.")
        return pd.DataFrame()

    df = pd.DataFrame(response.data)
    print(f"Data successfully retrieved from Supabase ({len(df)} rows)")

    # Sauvegarde optionnelle dans un fichier CSV
    output_dir = Path(__file__).parent / "energitic_pipeline"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "measurements_last_24hours.csv"
    df.to_csv(output_file, index=False)
    print(f"Data successfully saved to {output_file}")

    return df

if __name__ == "__main__":
    df = extract_data_to_dataframe()
    print(df.head())
