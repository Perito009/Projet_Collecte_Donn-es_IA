import pandas as pd

def clean_df(df, date_cols=None, unit_map=None):
	"""
	- date_cols: liste de colonnes à parser en datetime
	- unit_map: dict {'col': factor} pour convertir unités (multiplicateur)
	Retourne DataFrame nettoyé.
	"""
	if date_cols:
		for c in date_cols:
			df[c] = pd.to_datetime(df[c], errors='coerce')
	if unit_map:
		for c, f in unit_map.items():
			if c in df:
				df[c] = df[c].astype('float') * f
	return df
