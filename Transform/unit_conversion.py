import pandas as pd
import sys
from pathlib import Path
import logging

# Configuration du logging
logger = logging.getLogger(__name__)

# Ajouter le chemin racine du projet au PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from Extract.extract_db import extract_data_to_dataframe

def celsius_to_kelvin(celsius):
    """Convertit une température en Celsius en Kelvin."""
    if pd.isna(celsius):
        return None
    return celsius + 273.15

def kmh_to_ms(kmh):
    """Convertit une vitesse de km/h en m/s."""
    if pd.isna(kmh):
        return None
    return kmh / 3.6

def kwh_to_mwh(kwh):
    """Convertit l'énergie de kWh en MWh."""
    if pd.isna(kwh):
        return None
    return kwh / 1000

def normalize_units(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique les conversions d'unités au DataFrame :
    - Convertit 'temperature' de Celsius en Kelvin.
    - Convertit 'wind_speed' de km/h en m/s.
    - Convertit 'energie_kWh' en MWh.
    """
    try:
        logger.info("Début des conversions d'unités")
        
        if df.empty:
            logger.warning("DataFrame vide - aucune conversion effectuée")
            return df
        
        # Conversion température Celsius → Kelvin
        if "temperature" in df.columns:
            df["temperature_K"] = df["temperature"].apply(celsius_to_kelvin)
            logger.info(f"Température convertie: {df['temperature'].notna().sum()} valeurs")
        
        # Conversion vitesse vent km/h → m/s
        if "wind_speed" in df.columns:
            df["wind_speed_ms"] = df["wind_speed"].apply(kmh_to_ms)
            logger.info(f"Vitesse vent convertie: {df['wind_speed'].notna().sum()} valeurs")
        
        # Conversion énergie kWh → MWh
        if "energie_kWh" in df.columns:
            df["energie_mwh"] = df["energie_kWh"].apply(kwh_to_mwh)
            logger.info(f"Énergie convertie: {df['energie_kWh'].notna().sum()} valeurs")
        
        logger.info("Conversions d'unités terminées")
        return df
        
    except Exception as e:
        logger.error(f"Erreur lors de la conversion des unités: {e}")
        return df

def convert_units_from_db() -> pd.DataFrame:
    """
    Extrait les données depuis la base de données et applique les conversions d'unités.
    """
    try:
        logger.info("Extraction des données depuis la base de données...")
        df = extract_data_to_dataframe()
        
        if df.empty:
            logger.warning("Aucune donnée extraite de la base de données")
            return df
        
        logger.info(f"Données extraites: {len(df)} lignes")
        
        # Appliquer les conversions d'unités
        df_converted = normalize_units(df)
        
        return df_converted
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction et conversion: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Configuration du logging pour le test
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test avec extraction depuis la base de données
    print("=== Test de conversion d'unités ===")
    df_converted = convert_units_from_db()
    
    if not df_converted.empty:
        print(f"DataFrame converti - Shape: {df_converted.shape}")
        print(f"Colonnes: {df_converted.columns.tolist()}")
        print("\nAperçu des données:")
        print(df_converted.head())
    else:
        print("Aucune donnée à afficher")