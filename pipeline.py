from Extract import extract_api, extract_csv, extract_db
from Transform import transform_clean, transform_quality
from Load import load_postgres
from Graphics import dashboard_generator
from settings import *

def main(dry_run=True):
	"""
	Orchestre ETL minimal. Si dry_run=True, n'effectue pas de chargement DB.
	Retourne True si exécution OK.
	"""
	# Extract
	# weather = extract_api.fetch_weather(API_URL)
	# prod = extract_csv.read_production_csv(CSV_PATH)
	# sensors = extract_db.fetch_sensor_data(DB_CONN, "SELECT * FROM sensors;")
	# Transform
	# cleaned = transform_clean.clean_df(prod, date_cols=['timestamp'])
	# cleaned, report = transform_quality.quality_checks(cleaned)
	# Load
	if not dry_run:
		# load_postgres.load_dataframe(cleaned, 'measurements', PG_CONN)
		pass
	# Dashboard (example)
	dashboard_generator.generate_dashboard("<p>Exemple</p>", DASHBOARD_PATH)
	return True

if __name__ == '__main__':
	main(dry_run=True)