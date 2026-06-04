from pathlib import Path
import os
from datetime import datetime


# -----------------------------------
# BASE PATHS
# -----------------------------------

BASE_DIR = (

    Path(__file__)
    .resolve()
    .parents[2]
)

DATA_DIR = (

    BASE_DIR
    / "data"
)

EXPORT_DIR = (

    DATA_DIR
    / "exports"
)

DOCS_DIR = (

    BASE_DIR
    / "docs"
)

DASHBOARD_DIR = (

    BASE_DIR
    / "dashboard"
)

SEED_DIR = (

    DATA_DIR
    / "seeds"
)

DATABASE_DIR = (

    DATA_DIR
    / "database"
)

# -----------------------------------
# CREATE FOLDERS
# -----------------------------------

for folder in [

    EXPORT_DIR,
    DOCS_DIR,
    DATABASE_DIR

]:

    folder.mkdir(

        parents=True,

        exist_ok=True
    )


# -----------------------------------
# ENVIRONMENT
# -----------------------------------

def get_app_env():

    return os.getenv(

        "APP_ENV",

        "prod"
    )


# -----------------------------------
# DATABASES
# -----------------------------------

DATABASES = {

    "dev":

        DATABASE_DIR
        / "dev-trading-system.db",

    "test":

        DATABASE_DIR
        / "test-trading-system.db",

    "prod":

        DATABASE_DIR
        / "prod-trading-system.db"
}


def get_database_file():

    return DATABASES[

        get_app_env()
    ]


# -----------------------------------
# INPUT SOURCES
# -----------------------------------

INPUT_SOURCES = {

    "dev":

        SEED_DIR
        / "sample_transactions.csv",

    "test":

        SEED_DIR
        / "sample_transactions.csv",

    "prod":

        DASHBOARD_DIR
        / "trading_system.xlsx"
}


def get_input_source():

    return INPUT_SOURCES[

        get_app_env()
    ]


# -----------------------------------
# OUTPUT HELPERS
# -----------------------------------

def get_output_suffix():

    return get_app_env()


def get_timestamp():

    return datetime.now().strftime(

        "%Y-%m-%d_%H-%M"
    )