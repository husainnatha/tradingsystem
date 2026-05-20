from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# -----------------------------------
# DATABASE PATH
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

db_path = (
    BASE_DIR
    / "data"
    / "database"
    / "portfolio.db"
)

DATABASE_URL = f"sqlite:///{db_path}"

# -----------------------------------
# SQLALCHEMY ENGINE
# -----------------------------------

engine = create_engine(

    DATABASE_URL,

    echo=False
)

# -----------------------------------
# SESSION FACTORY
# -----------------------------------

SessionLocal = sessionmaker(

    bind=engine
)