import sys
import subprocess
from pathlib import Path
import pandas as pd
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_production_pipeline():
    """Exécute le script pour traiter le fichier de production."""
    try:
        logger.info("Lancement du script de traitement du fichier de production...")
        subprocess.run([sys.executable, "-m", "Loading.insert_prod"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Erreur lors de l'exécution du script de production: {e}")

def run_extract_db():
    """Exécute le script extract_db.py pour extraire les données de la base."""
    try:
        logger.info("Début de l'extraction depuis la base de données...")

        # Import direct pour récupérer le DataFrame
        from Extract.extract_db import extract_data_to_dataframe

        df = extract_data_to_dataframe()

        if df.empty:
            logger.warning("Aucune donnée extraite de la base de données")
            return None

        logger.info(f"✅ Extraction DB terminée. {len(df)} lignes extraites.")
        return df

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution de extract_db.py: {e}")
        return None

def run_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Exécute le nettoyage des données."""
    try:
        logger.info("Début du nettoyage des données...")

        from Transform.data_cleaning import clean_data_from_db

        df_clean = clean_data_from_db()

        if df_clean.empty:
            logger.warning("Aucune donnée après nettoyage")
            return df  # Retourne les données originales si échec

        logger.info(f"✅ Nettoyage terminé. {len(df_clean)} lignes traitées.")
        return df_clean

    except Exception as e:
        logger.error(f"❌ Erreur lors du nettoyage: {e}")
        return df  # Retourne les données originales en cas d'erreur

def run_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """Exécute la normalisation des dates."""
    try:
        logger.info("Début de la normalisation des dates...")

        from Transform.date_normalization import normalize_dates_from_db

        df_normalized = normalize_dates_from_db()

        if df_normalized.empty:
            logger.warning("Aucune donnée après normalisation")
            return df

        logger.info(f"✅ Normalisation des dates terminée.")
        return df_normalized

    except Exception as e:
        logger.error(f"❌ Erreur lors de la normalisation: {e}")
        return df

def run_unit_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """Exécute la conversion des unités."""
    try:
        logger.info("Début de la conversion des unités...")

        from Transform.unit_conversion import convert_units_from_db

        df_converted = convert_units_from_db()

        if df_converted.empty:
            logger.warning("Aucune donnée après conversion")
            return df

        logger.info(f"✅ Conversion des unités terminée.")
        return df_converted

    except Exception as e:
        logger.error(f"❌ Erreur lors de la conversion: {e}")
        return df

def run_transform_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Exécute toute la logique de transformation dans l'ordre correct."""
    logger.info("🚀 Démarrage du pipeline de transformation...")

    # Ordre correct du pipeline :
    # 1. Cleaning des données
    df = run_cleaning(df)

    # 2. Normalisation des dates
    df = run_normalization(df)

    # 3. Conversion des unités
    df = run_unit_conversion(df)

    logger.info("✨ Pipeline Transform terminé avec succès!")
    return df

def display_pipeline_summary(df: pd.DataFrame):
    """Affiche un résumé du pipeline."""
    print("\n" + "="*50)
    print("📊 RÉSUMÉ DU PIPELINE")
    print("="*50)
    print(f"📈 Nombre total d'enregistrements: {len(df)}")
    print(f"🏷️  Nombre de colonnes: {len(df.columns)}")
    print(f"📋 Colonnes disponibles: {list(df.columns)}")

    # Afficher les statistiques de base
    if not df.empty:
        print(f"\n📊 Aperçu des données:")
        print(df.head())

        # Informations sur les valeurs manquantes
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print(f"\n⚠️  Valeurs manquantes par colonne:")
            for col, count in missing_values[missing_values > 0].items():
                print(f"   - {col}: {count} valeurs manquantes")
        else:
            print(f"\n✅ Aucune valeur manquante détectée")

def main():
    """Exécute le pipeline complet selon la logique définie."""
    logger.info("🎯 Démarrage du pipeline complet...")

    # Étape 0: Vérification du fichier de production
    from Loading.insert_prod import get_current_production_file

    try:
        file_path = get_current_production_file()
        logger.info(f"Fichier de production trouvé : {file_path}")
        logger.info("Lancement du traitement du fichier de production...")
        run_production_pipeline()
    except FileNotFoundError:
        logger.info("Aucun fichier de production détecté. Lancement de l'extraction depuis la base de données...")

        # Étape 1: Extraction depuis la base de données
        df = run_extract_db()

        if df is None or df.empty:
            logger.error("❌ Échec de l'extraction des données. Arrêt du pipeline.")
            return

        print(f"\n📥 Données initiales extraites: {len(df)} lignes, {len(df.columns)} colonnes")

        # Étape 2: Transformation des données
        df = run_transform_pipeline(df)

        # Étape 3: Affichage du résumé
        display_pipeline_summary(df)

    logger.info("🎉 Pipeline terminé avec succès!")

if __name__ == "__main__":
    main()
