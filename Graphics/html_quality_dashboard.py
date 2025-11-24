import pandas as pd

from date_normalization import normalize_dates
from unit_conversion import convert_units
from enrichment import enrich_data
from data_cleaning import clean_data

from Graphics.dashboard_generator import generate_dashboard


def run_pipeline():
    # --- 1. Charger les données extraites ---
    df = pd.read_csv("../Extract/measurements last 24hours.csv")
    print("📥 Données chargées pour transformation")

    # --- 2. Normalisation des dates ---
    df = normalize_dates(df)

    # --- 3. Harmonisation des unités ---
    df = convert_units(df)

    # --- 4. Enrichissement (ID turbines, etc.) ---
    df = enrich_data(df)

    # --- 5. Nettoyage & détection anomalies ---
    df = clean_data(df)

    print("✨ Pipeline Transform terminé.")

    # --- 6. Génération du dashboard depuis df ---
    generate_dashboard(df)

    return df


if __name__ == "__main__":
    run_pipeline()
