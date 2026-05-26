from app.database.db import (
    engine
)

from app.database.models import (
    Base
)

print(
    "\nCreating database tables...\n"
)

print(
    "Dropping existing tables..."
)

Base.metadata.drop_all(
    bind=engine
)

Base.metadata.create_all(bind=engine)

print(
    "\nDatabase initialized.\n"
)