#!/bin/bash

# Créer le répertoire logs s'il n'existe pas
mkdir -p /workspaces/Projet_Collecte_Donn-es_IA/logs

# Se déplacer dans le répertoire du projet
cd /workspaces/Projet_Collecte_Donn-es_IA

# Exécuter le script Python et rediriger les logs
python3 main_pipeline.py >> /workspaces/Projet_Collecte_Donn-es_IA/logs/pipeline.log 2>&1

# Supprimer le dossier energetic_pipeline dans Extract après l'exécution du pipeline
rm -rf Extract/energetic_pipeline

echo "Le dossier Extract/energetic_pipeline a été supprimé."
