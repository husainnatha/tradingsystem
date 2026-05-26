from sqlalchemy import create_engine

from sqlalchemy.orm import (

    sessionmaker
)

from app.config.environment import (

    get_database_file
)

# -----------------------------------
# ENGINE
# -----------------------------------

engine = create_engine(

    f"sqlite:///{get_database_file()}"
)

# -----------------------------------
# SESSION
# -----------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)