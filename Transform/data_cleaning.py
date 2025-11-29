# Transform/data_cleaning.py
import pandas as pd
import logging
from Extract.extract_db import extract_data_to_dataframe

# Configuration du logging
logger = logging.getLogger(__name__)

def detect_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Détecte les valeurs aberrantes avec une méthode IQR simple.
    """
    df["energy_anomaly"] = False

    # Détection pour l'énergie
    if "energie_kWh" in df.columns and "turbin_id" in df.columns:
        for turbine in df["turbin_id"].unique():
            mask = df["turbin_id"] == turbine
            values = df[mask]["energie_kWh"].dropna()
            
            if len(values) >= 4:  # Minimum pour calculer les quartiles
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Marquer les outliers
                outliers_mask = mask & ((df["energie_kWh"] < lower_bound) | (df["energie_kWh"] > upper_bound))
                df.loc[outliers_mask, "energy_anomaly"] = True
                logger.info(f"Outliers détectés pour {turbine}: {outliers_mask.sum()}")

    return df

def fill_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige les valeurs manquantes.
    """
    # Énergie - imputation par médiane
    if "energie_kWh" in df.columns and "turbin_id" in df.columns:
        for turbine in df["turbin_id"].unique():
            mask = (df["turbin_id"] == turbine) & (df["energie_kWh"].isna())
            if mask.any():
                median_energy = df[df["turbin_id"] == turbine]["energie_kWh"].median()
                df.loc[mask, "energie_kWh"] = median_energy
                logger.info(f"Valeurs manquantes remplacées pour {turbine}: {mask.sum()}")

    # Variables binaires
    for col in ["arret_planifie", "arret_non_planifie"]:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df

def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige les outliers.
    """
    if "energy_anomaly" in df.columns and "turbin_id" in df.columns:
        for turbine in df["turbin_id"].unique():
            mask = (df["turbin_id"] == turbine) & (df["energy_anomaly"] == True)
            if mask.any():
                # Calculer la médiane sans les outliers
                normal_data = df[(df["turbin_id"] == turbine) & (df["energy_anomaly"] == False)]
                if not normal_data.empty:
                    median_energy = normal_data["energie_kWh"].median()
                    df.loc[mask, "energie_kWh"] = median_energy
                    logger.info(f"Outliers corrigés pour {turbine}: {mask.sum()}")

    return df

def clean_data_from_db() -> pd.DataFrame:
    """
    Nettoie les données depuis la base.
    """
    try:
        logger.info("Extraction des données...")
        df = extract_data_to_dataframe()
        
        if df.empty:
            return df

        logger.info("Nettoyage des données...")
        df = detect_outliers(df)
        df = fill_missing_values(df)
        df = handle_outliers(df)
        
        logger.info("Nettoyage terminé")
        return df
        
    except Exception as e:
        logger.error(f"Erreur: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    df_clean = clean_data_from_db()
    
    if not df_clean.empty:
        print(f"Données nettoyées: {df_clean.shape}")
        print(df_clean.head())
    else:
        print("Aucune donnée")