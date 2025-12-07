#!/bin/bash

# Créer le répertoire logs s'il n'existe pas
mkdir -p /workspaces/Projet_Collecte_Donn-es_IA/logs

# Se déplacer dans le répertoire du projet
cd /workspaces/Projet_Collecte_Donn-es_IA

# Exécuter le script Python et rediriger les logs
python3 main_pipeline.py >> /workspaces/Projet_Collecte_Donn-es_IA/logs/pipeline.log 2>&1

# Exécuter le script dashboard_generator.py et rediriger les logs
python3 ./Graphics/dashboard_generator.py >> /workspaces/Projet_Collecte_Donn-es_IA/logs/pipeline.log 2>&1

# Supprimer le dossier energitic_pipeline dans Extract après l'exécution du pipeline
rm -rf /workspaces/Projet_Collecte_Donn-es_IA/Extract/energitic_pipeline

echo "Le dossier Extract/energitic_pipeline a été supprimé."