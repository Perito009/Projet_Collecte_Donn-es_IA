import sys
from pathlib import Path
import pandas as pd
import pytz
import logging

# Configuration du logging
logger = logging.getLogger(__name__)

# Ajouter le chemin racine du projet au PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from Extract.extract_db import extract_data_to_dataframe

def normalize_timestamp_column(df: pd.DataFrame, ts_column: str = "ts_utc") -> pd.DataFrame:
    """
    Normalise une colonne de timestamp en :
    1. Convertissant en datetime (en gérant les erreurs).
    2. Convertissant au fuseau horaire Europe/Paris.
    3. Retournant les timestamps formatés en ISO 8601 avec offset.
    
    Args:
        df: DataFrame contenant les données
        ts_column: Nom de la colonne timestamp à normaliser (par défaut "ts_utc")
    
    Returns:
        DataFrame avec la colonne timestamp normalisée
    """
    try:
        logger.info(f"Début de la normalisation de la colonne '{ts_column}'")
        
        # Vérifier si la colonne existe
        if ts_column not in df.columns:
            logger.warning(f"Colonne '{ts_column}' non trouvée. Colonnes disponibles: {df.columns.tolist()}")
            return df
        
        # Vérifier si le DataFrame n'est pas vide
        if df.empty:
            logger.warning("DataFrame vide - aucune normalisation effectuée")
            return df
        
        # Sauvegarder le nombre de valeurs manquantes avant traitement
        initial_missing = df[ts_column].isna().sum()
        initial_count = len(df)
        
        # Convertir la colonne en datetime, en gérant les erreurs
        df[ts_column] = pd.to_datetime(df[ts_column], errors='coerce', utc=True)
        
        # Compter les conversions échouées
        failed_conversions = df[ts_column].isna().sum() - initial_missing
        if failed_conversions > 0:
            logger.warning(f"{failed_conversions} conversions de timestamp ont échoué")
        
        # Convertir au fuseau horaire Europe/Paris
        paris_tz = pytz.timezone('Europe/Paris')
        
        # Localiser en UTC puis convertir en Europe/Paris
        df[ts_column] = df[ts_column].dt.tz_convert(paris_tz)
        
        # Formater en ISO 8601 avec offset
        df[ts_column] = df[ts_column].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
        
        # Ajouter une colonne formatée pour l'affichage
        df[f"{ts_column}_formatted"] = pd.to_datetime(df[ts_column]).dt.strftime('%Y-%m-%d %H:%M:%S %Z')
        
        # Log des résultats
        final_missing = df[ts_column].isna().sum()
        logger.info(f"Normalisation terminée: {initial_count - final_missing} timestamps traités, {final_missing} valeurs manquantes")
        
    except Exception as e:
        logger.error(f"Erreur lors de la normalisation de la colonne '{ts_column}': {e}")
    
    return df

def detect_timestamp_columns(df: pd.DataFrame) -> list:
    """
    Détecte automatiquement les colonnes de type timestamp dans le DataFrame
    
    Args:
        df: DataFrame à analyser
    
    Returns:
        Liste des noms de colonnes détectées comme timestamps
    """
    timestamp_columns = []
    
    # Colonnes communes pour les timestamps
    common_timestamp_names = [
        'ts_utc', 'timestamp', 'date', 'datetime', 'time', 
        'created_at', 'updated_at', 'measurement_time'
    ]
    
    for col in df.columns:
        # Vérifier par nom
        if any(name in col.lower() for name in ['time', 'date', 'ts', 'timestamp']):
            timestamp_columns.append(col)
        # Vérifier par type de données
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            timestamp_columns.append(col)
    
    # Ajouter les colonnes communes si elles existent
    for col in common_timestamp_names:
        if col in df.columns and col not in timestamp_columns:
            timestamp_columns.append(col)
    
    logger.info(f"Colonnes timestamp détectées: {timestamp_columns}")
    return timestamp_columns

def normalize_all_timestamps(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise automatiquement toutes les colonnes timestamp détectées
    
    Args:
        df: DataFrame contenant les données
    
    Returns:
        DataFrame avec toutes les colonnes timestamp normalisées
    """
    timestamp_columns = detect_timestamp_columns(df)
    
    for ts_col in timestamp_columns:
        df = normalize_timestamp_column(df, ts_col)
    
    return df

def normalize_dates_from_db(ts_column: str = "ts_utc") -> pd.DataFrame:
    """
    Extrait les données depuis la base de données et normalise les timestamps
    
    Args:
        ts_column: Nom de la colonne timestamp à normaliser
    
    Returns:
        DataFrame avec les timestamps normalisés
    """
    try:
        logger.info("Extraction des données depuis la base de données...")
        df = extract_data_to_dataframe()
        
        if df.empty:
            logger.warning("Aucune donnée extraite de la base de données")
            return df
        
        logger.info(f"Données extraites: {len(df)} lignes, {len(df.columns)} colonnes")
        
        # Normaliser la colonne timestamp spécifiée
        df_normalized = normalize_timestamp_column(df, ts_column)
        
        return df_normalized
        
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction et normalisation: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Configuration du logging pour le test
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Test avec extraction depuis la base de données
    print("=== Test de normalisation avec données de la base de données ===")
    df_normalized = normalize_dates_from_db("ts_utc")
    
    if not df_normalized.empty:
        print(f"\nDataFrame normalisé - Shape: {df_normalized.shape}")
        print(f"\nColonnes disponibles: {df_normalized.columns.tolist()}")
        
        # Afficher les premières lignes avec les timestamps normalisés
        if "ts_utc" in df_normalized.columns:
            print(f"\nAperçu des timestamps normalisés:")
            print(df_normalized[["ts_utc", "ts_utc_formatted"]].head(10))
        else:
            print("\nAperçu des données:")
            print(df_normalized.head(10))
            
        # Information sur les timezones
        timestamp_cols = detect_timestamp_columns(df_normalized)
        print(f"\nColonnes timestamp détectées: {timestamp_cols}")
    else:
        print("Aucune donnée à afficher")