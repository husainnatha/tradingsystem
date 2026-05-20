from pathlib import Path

import pandas as pd

from app.engine.matching_engine import (
    get_same_day_matches,
    get_thirty_day_matches,
    get_section_104_pool
)

from app.engine.disposal_ledger import (
    build_disposal_ledger
)

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

export_dir = (
    BASE_DIR
    / "exports"
    / "matching_audit"
)

export_dir.mkdir(
    parents=True,
    exist_ok=True
)

print(
    f"\nExport directory:\n{export_dir}\n"
)

# -----------------------------------
# SAME-DAY MATCHES
# -----------------------------------

same_day_results = (
    get_same_day_matches()
)

same_day_df = pd.DataFrame(
    same_day_results[
        "matches"
    ]
)

same_day_path = (
    export_dir
    / "same_day_matches.csv"
)

same_day_df.to_csv(
    same_day_path,
    index=False
)

print(
    f"Exported:\n{same_day_path}"
)

# -----------------------------------
# THIRTY-DAY MATCHES
# -----------------------------------

thirty_day_results = (
    get_thirty_day_matches()
)

thirty_day_df = pd.DataFrame(
    thirty_day_results[
        "thirty_day_matches"
    ]
)

thirty_day_path = (
    export_dir
    / "thirty_day_matches.csv"
)

thirty_day_df.to_csv(
    thirty_day_path,
    index=False
)

print(
    f"Exported:\n{thirty_day_path}"
)

# -----------------------------------
# SECTION 104 DISPOSALS
# -----------------------------------

s104_results = (
    get_section_104_pool()
)

s104_df = pd.DataFrame(
    s104_results[
        "section_104_disposals"
    ]
)

s104_path = (
    export_dir
    / "section_104_disposals.csv"
)

s104_df.to_csv(
    s104_path,
    index=False
)

print(
    f"Exported:\n{s104_path}"
)

# -----------------------------------
# DISPOSAL LEDGER
# -----------------------------------

ledger = build_disposal_ledger()

ledger_df = pd.DataFrame(
    ledger
)

ledger_path = (
    export_dir
    / "disposal_ledger.csv"
)

ledger_df.to_csv(
    ledger_path,
    index=False
)

print(
    f"Exported:\n{ledger_path}"
)

print(
    "\nMatching audit export complete.\n"
)