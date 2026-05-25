from pathlib import Path


# -----------------------------------
# PROJECT ROOT
# -----------------------------------

BASE_DIR = (

    Path(__file__)

    .resolve()

    .parents[2]
)

# -----------------------------------
# CORE DIRECTORIES
# -----------------------------------

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

TEST_DIR = (

    BASE_DIR
    / "tests"
)

# -----------------------------------
# FILES
# -----------------------------------

TRADING_SYSTEM_FILE = (

    DASHBOARD_DIR
    / "trading_system.xlsx"
)

DATABASE_FILE = (

    DATA_DIR
    / "portfolio.db"
)