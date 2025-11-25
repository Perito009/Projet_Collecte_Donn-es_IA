import sys
from pathlib import Path
import pandas as pd

try:
    # Exposer les fonctions courantes au niveau du package (import sûr)
    from .date_normalization import normalize_dates  # type: ignore
    from .unit_conversion import convert_units      # type: ignore
    from .enrichment import enrich_data            # type: ignore
    from .data_cleaning import clean_data          # type: ignore
except Exception:
    # Ne pas échouer à l'import du package si un module lève une erreur.
    # Les modules restent importables explicitement (ex: from Transform.date_normalization import normalize_dates).
    pass

__all__ = [
    "normalize_dates",
    "convert_units",
    "enrich_data",
    "clean_data",
]

from Transform.date_normalization import normalize_dates
from Transform.unit_conversion import convert_units
from Transform.enrichment import enrich_data
from Transform.data_cleaning import clean_data

from Graphics.dashboard_generator import generate_dashboard


def _load_df_from_extract():
    """
    Tente d'importer le module Extract.extract_db depuis la racine du workspace
    et récupérer la DataFrame déjà construite (variable `df`) ou appeler une
    fonction publique si elle existe.
    """
    root = Path(__file__).resolve().parent  # workspace root
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)

    try:
        import Extract.extract_db as extract_db  # type: ignore
    except Exception as e:
        print(f"⚠️ Impossible d'importer Extract.extract_db : {e}")
        return None

    # Priorité : variable df, sinon fonctions usuelles si présentes
    if hasattr(extract_db, "df"):
        return getattr(extract_db, "df")
    for fn in ("get_recent_df", "fetch_last_24h", "fetch_df"):
        if hasattr(extract_db, fn):
            try:
                return getattr(extract_db, fn)()
            except Exception as e:
                print(f"⚠️ Appel de {fn}() a échoué : {e}")
                return None
    return None


def run_pipeline():
    # --- 0. Obtenir les données (Extract) ---
    df = _load_df_from_extract()
    if df is None:
        # fallback : lire le CSV local comme avant
        csv_path = Path(__file__).resolve().parent / "Extract" / "measurements last 24hours.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            print("📥 Données chargées depuis CSV (fallback)")
        else:
            raise FileNotFoundError("Aucune source de données disponible (Extract import failed and CSV absent).")

    print("📥 Données chargées pour transformation")

    # --- 1. Normalisation des dates ---
    df = normalize_dates(df)

    # --- 2. Harmonisation des unités ---
    df = convert_units(df)

    # --- 3. Enrichissement (ID turbines, etc.) ---
    df = enrich_data(df)

    # --- 4. Nettoyage & détection anomalies ---
    df = clean_data(df)

    print("✨ Pipeline Transform terminé.")

    # --- 5. Génération du dashboard depuis df ---
    try:
        generate_dashboard(df)
    except Exception as e:
        print(f"⚠️ Génération du dashboard a échoué : {e}")

    return df


if __name__ == "__main__":
    run_pipeline()
