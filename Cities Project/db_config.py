from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Erst normale .env laden (für ENVIRONMENT)
load_dotenv()

env = os.getenv("ENVIRONMENT")

# Dann je nach Umgebung richtige Datei laden
if env == "gcp":
    load_dotenv(".env.gcp")
else:
    load_dotenv(".env.local")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)