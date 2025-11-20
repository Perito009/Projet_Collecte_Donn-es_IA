from dotenv import load_dotenv
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from pathlib import Path

# load .env next to this file
env_path = Path(__file__).with_name(".env")
load_dotenv(env_path)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(
    url,
    key,
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
        schema="public",
    )
)

response = (
    supabase.table("raw_measurements")
    .select("*")
    .execute()
)

print(response)