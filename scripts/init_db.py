from app.database.db import (
    engine
)

from app.database.models import (
    Base
)

print(
    "\nCreating database tables...\n"
)

Base.metadata.create_all(bind=engine)

print(
    "\nDatabase initialized.\n"
)