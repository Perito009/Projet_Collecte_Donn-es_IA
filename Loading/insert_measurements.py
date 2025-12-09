import csv
from pathlib import Path
from Extract.extract_db import init_supabase_client  # Importer la fonction depuis extract_db.py

def load_csv_data(file_path):
    """Charge les données depuis un fichier CSV."""
    data = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data

def upsert_measurements_into_supabase(data):
    """Met à jour ou insère les données dans la table raw_measurements de Supabase."""
    supabase = init_supabase_client()
    response = supabase.table("raw_measurements").upsert(data, on_conflict="meas_id").execute()
    return response

def main():
    # Chemin vers le fichier CSV
    csv_file_path = Path("Extract/energitic_pipeline/measurements_last_24hours.csv")

    # Charger les données depuis le fichier CSV
    data = load_csv_data(csv_file_path)

    if not data:
        print("Aucune donnée trouvée dans le fichier CSV.")
        return

    # Mettre à jour/insérer les données dans Supabase
    print(f"Upsert de {len(data)} lignes dans la table raw_measurements...")
    response = upsert_measurements_into_supabase(data)
    print("Upsert terminé !")
    print(response)

if __name__ == "__main__":
    main()
