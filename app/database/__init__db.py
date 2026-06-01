from app.database.db import engine
from app.database.models import Base

print("Creating database tables...")

Base.metadata.create_all(engine)

print("Database initialisation complete.")