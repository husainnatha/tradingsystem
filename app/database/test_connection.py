from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

db_path = BASE_DIR / "data" / "database" / "portfolio.db"

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)

connection = engine.connect()

print("Database connection successful.")
print(f"Database location: {db_path}")

connection.close()