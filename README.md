# Projet Collecte de Données pour Maintenance Prédictive - EnergiTech

## Description
Ce projet vise à concevoir un pipeline ETL pour collecter, nettoyer et stocker des données hétérogènes afin d'alimenter un modèle d'IA de maintenance prédictive pour les turbines éoliennes d'EnergiTech.

## Prérequis
- Python 3.10+
- PostgreSQL 14+
- Bibliothèques Python : `requests`, `pandas`, `psycopg2`, `matplotlib`

## Installation
1. Cloner le dépôt :
   ```bash
   git clone https://github.com/votre-depot/Projet_Collecte_Données_IA.git
   ```

## Guide d'installation et d'exécution minimal

Projet ETL minimal - instructions rapides.

1. Créer un virtualenv et installer dépendances:
   ```bash
   pip install -r requirements.txt
   ```

2. Adapter settings.py (conn strings, chemins).

3. Lancer le pipeline en dry-run:
   ```bash
   python pipeline.py
   ```

4. Exécuter les tests:
   ```bash
   pytest -q
   ```
