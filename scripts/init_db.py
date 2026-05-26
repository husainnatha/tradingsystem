from app.database.database import (
    engine
)

from app.database.models import (
    Base
)

print(
    "\nCreating database tables...\n"
)

Base.metadata.create_all(

    bind=engine
)

print(
    "\nDatabase initialized.\n"
)