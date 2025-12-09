#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère un DataFrame de production journalière par turbine pour un mois donné et le sauvegarde dans un fichier CSV.
Entrées : année (AAAA) et mois (MM).
Sortie  : DataFrame et fichier CSV dans le dossier 'energitic-pipeline'.
Exemple pour lancer le script : python extract_csv.py 2025 10
Spécifications colonnes :
date;turbin_id;energie_kWh;arret_planifie;arret_non_planifie
- turbin_id ∈ {T001, T002}
- energie_kWh : valeur réaliste (aléatoire) de production journalière
- arret_planifie, arret_non_planifie : 0/1 (mutuellement exclusifs)
- Certaines lignes peuvent contenir des valeurs manquantes (champs vides)
"""
import argparse
import calendar
from datetime import date
from pathlib import Path
import random
import pandas as pd
from typing import Tuple

# Capacités nominales (MW) par turbine — valeurs plausibles modernes
RATED_MW = {
    "T001": 3.2,  # 3.2 MW
    "T002": 2.8,  # 2.8 MW
}

# Moyennes de facteur de charge par mois (hémisphère Nord, ordre 1..12)
MONTHLY_CF_MEAN = {
    1: 0.42, 2: 0.40, 3: 0.38, 4: 0.35,
    5: 0.30, 6: 0.28, 7: 0.25, 8: 0.27,
    9: 0.32, 10: 0.36, 11: 0.40, 12: 0.43,
}

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def daily_capacity_factor(month: int) -> float:
    mean = MONTHLY_CF_MEAN.get(month, 0.33)
    cf = random.gauss(mu=mean, sigma=0.10)
    return clamp(cf, 0.0, 1.0)

def simulate_outages() -> Tuple[int, int]:
    planned = 1 if random.random() < 0.02 else 0
    if planned == 1:
        return 1, 0
    unplanned = 1 if random.random() < 0.01 else 0
    return 0, unplanned

def maybe_make_missing(row: dict) -> dict:
    r = random.random()
    if r < 0.05:
        row["energie_kWh"] = None
    if random.random() < 0.02:
        row["arret_planifie"] = None
    if random.random() < 0.02:
        row["arret_non_planifie"] = None
    return row

def compute_daily_energy_kwh(turbine: str, y: int, m: int, planned: int, unplanned: int) -> float:
    if planned == 1 or unplanned == 1:
        return 0.0
    cf = daily_capacity_factor(m)
    rated_mw = RATED_MW[turbine]
    energy = cf * rated_mw * 24.0 * 1000.0
    jitter = random.uniform(0.97, 1.03)
    energy *= jitter
    return energy

def extract_data_to_csv(year: int, month: int) -> pd.DataFrame:
    """
    Génère un DataFrame de production journalière par turbine pour un mois donné et le sauvegarde dans un fichier CSV.
    """
    if not (1 <= month <= 12):
        raise ValueError("Le mois doit être dans [1..12].")
    if year < 1:
        raise ValueError("L'année doit être un entier positif (AAAA).")

    nb_days = calendar.monthrange(year, month)[1]
    days = [date(year, month, d) for d in range(1, nb_days + 1)]
    turbines = ["T001", "T002"]

    data = []
    for d in days:
        for t in turbines:
            planned, unplanned = simulate_outages()
            energy = compute_daily_energy_kwh(t, year, month, planned, unplanned)
            row = {
                "date": d.strftime("%Y-%m-%d"),
                "turbin_id": t,
                "energie_kWh": energy,
                "arret_planifie": planned,
                "arret_non_planifie": unplanned,
            }
            row = maybe_make_missing(row)
            data.append(row)

    df = pd.DataFrame(data)

    # Sauvegarder dans un fichier CSV
    output_dir = Path(__file__).parent / "energitic_pipeline"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"production_{year:04d}_{month:02d}.csv"
    df.to_csv(output_file, index=False, sep=';')

    print(f"Data successfully saved to {output_file}")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Génère un DataFrame de production journalière par turbine.")
    parser.add_argument("annee", type=int, help="Année au format AAAA (ex: 2025)")
    parser.add_argument("mois", type=int, help="Mois au format MM (1-12)")
    parser.add_argument("--seed", type=int, default=None, help="Graine aléatoire (optionnelle) pour reproductibilité")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    df = extract_data_to_csv(args.annee, args.mois)
    print("\nData successfully stored in DataFrame")
    print(df.head())
