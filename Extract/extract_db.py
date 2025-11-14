import pandas as pd
from sqlalchemy import create_engine

def fetch_sensor_data(conn_string, query):
	"""
	Exécute query et renvoie un DataFrame.
	Exemple de conn_string: 'postgresql+psycopg2://user:pass@host/db'
	"""
	engine = create_engine(conn_string)
	with engine.connect() as conn:
		return pd.read_sql_query(query, conn)
