import csv
from pathlib import Path
from datetime import datetime
from Extract.extract_db import init_supabase_client

def get_current_production_file():
    """Trouve le fichier de production correspondant au mois et à l'année actuels."""
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    file_name = f"production_{year}_{month:02d}.csv"
    file_path = Path(f"Extract/energitic_pipeline/{file_name}")

    if not file_path.exists():
        raise FileNotFoundError(f"Le fichier {file_name} n'existe pas dans le répertoire Extract/energitic_pipeline/.")

    return file_path

def load_and_clean_production_data(file_path):
    """Charge et nettoie les données du fichier de production."""
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            # Nettoyage et transformation des données
            cleaned_row = {
                "turbine_id": row['turbin_id'],
                "ts_utc": f"{row['date']} 00:00:00",  # Ajout de l'heure pour correspondre au format TIMESTAMP
                "consumption_kwh": float(row.get('energie_kWh', 0)) if row.get('energie_kWh') else None,
            }
            data.append(cleaned_row)
    return data

def upsert_production_into_supabase(data):
    """Met à jour ou insère les données de production dans la table raw_measurements de Supabase."""
    supabase = init_supabase_client()
    response = supabase.table("raw_measurements").upsert(data, on_conflict="turbine_id, ts_utc").execute()
    return response

def main():
    try:
        # Trouver le fichier de production pour le mois et l'année actuels
        file_path = get_current_production_file()
        print(f"Fichier trouvé : {file_path}")

        # Charger et nettoyer les données du fichier de production
        data = load_and_clean_production_data(file_path)

        if not data:
            print("Aucune donnée trouvée dans le fichier de production.")
            return

        # Mettre à jour/insérer les données dans Supabase
        print(f"Upsert de {len(data)} lignes dans la table raw_measurements...")
        response = upsert_production_into_supabase(data)
        print("Upsert terminé !")
        print(response)

    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    main()
