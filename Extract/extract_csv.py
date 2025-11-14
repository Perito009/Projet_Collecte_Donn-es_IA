import pandas as pd

def read_production_csv(path, **kwargs):
	"""
	Lit un CSV de production et retourne un DataFrame pandas.
	kwargs passent à pd.read_csv.
	"""
	return pd.read_csv(path, **kwargs)
