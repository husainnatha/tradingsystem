from pathlib import Path

import pandas as pd

from app.engine.transaction_service import (
    add_transaction
)

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

csv_path = (

    BASE_DIR
    / "data"
    / "seeds"
    / "sample_transactions.csv"
)

# -----------------------------------
# LOAD CSV
# -----------------------------------

print(

    f"\nLoading seed data:\n"
    f"{csv_path}\n"
)

df = pd.read_csv(

    csv_path,

    dayfirst=True
)

print(

    "Seed data loaded successfully.\n"
)

# -----------------------------------
# VALIDATE COLUMNS
# -----------------------------------

required_columns = [

    "trade_date",
    "account",
    "symbol",
    "action",
    "quantity",
    "trade_currency",
    "trade_price",
    "fees",
    "fx_rate_to_gbp",
    "notes"
]

missing_columns = [

    col

    for col in required_columns

    if col not in df.columns
]

if missing_columns:

    raise Exception(

        f"Missing columns: "
        f"{missing_columns}"
    )

print(
    "Column validation passed.\n"
)

# -----------------------------------
# IMPORT TRANSACTIONS
# -----------------------------------

for index, row in df.iterrows():

    try:

        trade_date = pd.to_datetime(

            row["trade_date"],

            dayfirst=True

        ).date()

        account = str(

            row["account"]

        ).upper()

        symbol = str(

            row["symbol"]

        ).upper()

        action = str(

            row["action"]

        ).upper()

        quantity = float(

            row["quantity"]
        )

        trade_currency = str(

            row["trade_currency"]

        ).upper()

        trade_price = float(

            row["trade_price"]
        )

        fees = (

            0

            if pd.isna(
                row["fees"]
            )

            else float(
                row["fees"]
            )
        )

        fx_rate_to_gbp = (

            1.0

            if pd.isna(
                row[
                    "fx_rate_to_gbp"
                ]
            )

            else float(
                row[
                    "fx_rate_to_gbp"
                ]
            )
        )

        notes = (

            ""

            if pd.isna(
                row["notes"]
            )

            else str(
                row["notes"]
            )
        )

        print(

            f"Importing row "
            f"{index + 2}: "

            f"{account} | "

            f"{symbol} | "

            f"{action} | "

            f"{quantity}"
        )

        add_transaction(

            trade_date=trade_date,

            account=account,

            symbol=symbol,

            action=action,

            quantity=quantity,

            trade_currency=
                trade_currency,

            trade_price=
                trade_price,

            fees=fees,

            fx_rate_to_gbp=
                fx_rate_to_gbp,

            notes=notes
        )

    except Exception as e:

        print(

            f"Error processing row "
            f"{index + 2}: {e}"
        )

print(
    "\nSeed import complete.\n"
)