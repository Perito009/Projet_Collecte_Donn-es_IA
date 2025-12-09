#!/bin/bash

echo "Démarrage du pipeline..."

# Créer le répertoire logs s'il n'existe pas
mkdir -p /workspaces/Projet_Collecte_Donn-es_IA/logs

# Se déplacer dans le répertoire du projet
cd /workspaces/Projet_Collecte_Donn-es_IA
echo "Répertoire du projet : $(pwd)"
echo "Suppression du fichier dashboard.html et wind_speed_hist.png s'il existe..."
# Supprimer le fichier dashboard.html s'il existe
rm -rf /workspaces/Projet_Collecte_Donn-es_IA/dashboard.html
echo "Suppression du fichier wind_speed_hist.png..."
rm -rf /workspaces/Projet_Collecte_Donn-es_IA/wind_speed_hist.png

echo "Exécution du script main_pipeline.py..."
# Exécuter le script Python et rediriger les logs
python3 main_pipeline.py >> /workspaces/Projet_Collecte_Donn-es_IA/logs/pipeline.log 2>&1

echo "Exécution du script dashboard_generator.py..."

# Exécuter le script dashboard_generator.py et rediriger les logs
python3 ./Graphics/dashboard_generator.py >> /workspaces/Projet_Collecte_Donn-es_IA/logs/pipeline.log 2>&1

echo "Suppression du dossier Extract/energitic_pipeline..."
# Supprimer le dossier energitic_pipeline dans Extract après l'exécution du pipeline
rm -rf /workspaces/Projet_Collecte_Donn-es_IA/Extract/energitic_pipeline


echo "Lancement du serveur HTTP..."
# Lancer un serveur HTTP pour servir le contenu du répertoire Graphics
python3 -m http.server