import pandas as pd

def quality_checks(df):
	"""
	Retourne (df_clean, report) où report est un dict d'indicateurs simples.
	Exemples: taux_missing par colonne, min/max valeurs.
	"""
	report = {}
	report['missing_percent'] = (df.isna().mean() * 100).to_dict()
	report['rows'] = len(df)
	# exemple simple: supprimer lignes sans timestamp si existant
	if 'timestamp' in df.columns:
		df = df.dropna(subset=['timestamp'])
	return df, report
