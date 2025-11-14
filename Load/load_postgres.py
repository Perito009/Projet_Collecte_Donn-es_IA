from sqlalchemy import create_engine

def load_dataframe(df, table_name, conn_string, if_exists='append', index=False):
	"""
	Charge df dans PostgreSQL. Conn_string au format SQLAlchemy.
	"""
	engine = create_engine(conn_string)
	df.to_sql(table_name, engine, if_exists=if_exists, index=index)
