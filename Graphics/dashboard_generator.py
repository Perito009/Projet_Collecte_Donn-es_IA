import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path
# Ajouter le chemin racine du projet au PYTHONPATH
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from Extract.extract_db import extract_data_to_dataframe

def read_log_file(log_path):
    """Lit le contenu d'un fichier de log et retourne les dernières lignes."""
    try:
        with open(log_path, 'r') as f:
            log_content = f.read()
        # Retourner les 50 dernières lignes pour éviter un contenu trop long
        return "<pre>" + "\n".join(log_content.splitlines()[-50:]) + "</pre>"
    except FileNotFoundError:
        return "<p>Fichier de log non trouvé.</p>"
    except Exception as e:
        return f"<p>Erreur lors de la lecture du fichier de log: {str(e)}</p>"

def generate_dashboard(df, output_html="dashboard.html"):
    """
    Génère un dashboard HTML à partir d’un DataFrame.
    """
    # Vérification du type
    if not isinstance(df, pd.DataFrame):
        raise TypeError("❌ generate_dashboard() attend un DataFrame en argument.")
    print("📄 DataFrame reçu, génération du dashboard...\n")

    # Aperçu
    print("=== Aperçu du DataFrame ===")
    print(df.head())

    # Statistiques
    print("\n=== Statistiques ===")
    print(df.describe(include="all"))

    # Histogramme
    hist_path = "wind_speed_hist.png"
    if "wind_speed_mps" in df.columns:
        plt.figure()
        plt.hist(df["wind_speed_mps"].dropna(), bins=20)
        plt.title("Répartition de la vitesse du vent (m/s)")
        plt.xlabel("Vitesse du vent (m/s)")
        plt.ylabel("Fréquence")
        plt.savefig(hist_path)
        plt.close()
        print(f"📊 Histogramme généré : {hist_path}")
    else:
        print("⚠️ Aucune colonne 'wind_speed_mps' → histogramme non généré.")

    # Chemin vers le fichier de log
    log_path = project_root / "logs" / "pipeline.log"
    log_content = read_log_file(log_path)

    # Construction du tableau HTML
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Dashboard Qualité des Données</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 30px;
                    background: #fafafa;
                }}
                h1, h2 {{
                    color: #333;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background: #eee;
                }}
                img {{
                    margin-top: 20px;
                    max-width: 600px;
                }}
                #log-section {{
                    background: #f8f8f8;
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin-top: 20px;
                    border-radius: 5px;
                    max-height: 300px;
                    overflow-y: auto;
                }}
            </style>
        </head>
        <body>
            <h1>Dashboard Qualité des Données</h1>
            <h2>Aperçu du Dataset</h2>
            {df.to_html(index=False)}
            <h2>Histogramme — Vitesse du vent</h2>
            {f'<img src="{hist_path}">' if os.path.exists(hist_path) else "<p>Aucun histogramme disponible.</p>"}
            <h2>Logs du Pipeline</h2>
            <div id="log-section">
                {log_content}
            </div>
        </body>
        </html>
        """)
    print(f"\n📁 Dashboard généré : {output_html}")

def generate_dashboard_from_db(output_html="dashboard.html"):
    """
    Génère un dashboard HTML à partir des données de extract_db.
    """
    df = extract_data_to_dataframe()
    generate_dashboard(df, output_html)

if __name__ == "__main__":
    generate_dashboard_from_db()
    print("\n✅ Dashboard généré avec succès !")
