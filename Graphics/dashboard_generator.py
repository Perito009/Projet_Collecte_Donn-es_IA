import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_dashboard(df, output_html="dashboard.html"):
    """
    Génère un dashboard HTML à partir d’un DataFrame.
    Aucun fichier CSV n’est lu dans cette version.
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
    if "wind_speed" in df.columns:
        plt.figure()
        plt.hist(df["wind_speed"].dropna(), bins=20)
        plt.title("Répartition de la vitesse du vent")
        plt.xlabel("Vitesse du vent")
        plt.ylabel("Fréquence")
        plt.savefig(hist_path)
        plt.close()
        print(f"📊 Histogramme généré : {hist_path}")
    else:
        print("⚠️ Aucune colonne 'wind_speed' → histogramme non généré.")

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
            </style>
        </head>
        <body>

            <h1>Dashboard Qualité des Données</h1>

            <h2>Aperçu du Dataset</h2>
            {df.to_html(index=False)}

            <h2>Histogramme — Vitesse du vent</h2>
            {f'<img src="{hist_path}">' if os.path.exists(hist_path) else "<p>Aucun histogramme disponible.</p>"}

        </body>
        </html>
        """)

    print(f"\n📁 Dashboard généré : {output_html}")
