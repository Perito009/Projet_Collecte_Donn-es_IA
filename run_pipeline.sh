#!/bin/bash

# Créer le répertoire logs s'il n'existe pas
mkdir -p /workspaces/Projet_Collecte_Donn-es_IA/logs

# Se déplacer dans le répertoire du projet
cd /workspaces/Projet_Collecte_Donn-es_IA

# Exécuter le script Python et rediriger les logs
python3 main_pipeline.py >> /workspaces/Projet_Collecte_Donn-es_IA/logs/pipeline.log 2>&1
