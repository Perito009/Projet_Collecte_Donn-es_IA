import os
from dotenv import load_dotenv
import psycopg

# Charge le .env présent dans le même dossier
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
	raise RuntimeError("DATABASE_URL non défini dans Extract/.env")

def get_conn():
	"""
	Renvoie une connexion psycopg. Pour Supabase, on exige généralement SSL.
	psycopg accepte l'URL de connexion directement ; si besoin ajoute '?sslmode=require'.
	"""
	url = DATABASE_URL
	if "sslmode=" not in url:
		# Forcer SSL when connecting to Supabase
		sep = "&" if "?" in url else "?"
		url = f"{url}{sep}sslmode=require"
	# Retourne une connexion : caller doit gérer le context manager
	return psycopg.connect(url)

def test_connection():
	"""Test simple qui exécute SELECT 1."""
	with get_conn() as conn:
		with conn.cursor() as cur:
			cur.execute("SELECT 1")
			row = cur.fetchone()
			return bool(row and row[0] == 1)

if __name__ == "__main__":
	import sys
	ok = test_connection()
	print("Connexion OK" if ok else "Connexion échouée")
	sys.exit(0 if ok else 2)
