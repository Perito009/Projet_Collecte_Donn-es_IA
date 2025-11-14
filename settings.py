import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

API_URL = "https://api.meteo.exemple/v1/data"
CSV_PATH = os.path.join(BASE_DIR, "data", "production.csv")
DB_CONN = "postgresql+psycopg2://user:pass@localhost/dbname"
PG_CONN = DB_CONN
DASHBOARD_PATH = os.path.join(BASE_DIR, "Graphics", "dashboard.html")
