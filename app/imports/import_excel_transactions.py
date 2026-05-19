from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.database.db import engine
from app.database.models import Account
from app.engine.transaction_service import add_transaction


BASE_DIR = Path(__file__).resolve().parents[2]

excel_path = BASE_DIR / "dashboard" / "trading_system.xlsx"

print(f"\nLoading workbook:\n{excel_path}\n")

df = pd.read_excel(
    excel_path,
    sheet_name="transactions"
)

print("Workbook loaded successfully.\n")

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
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    raise Exception(
        f"Missing columns: {missing_columns}"
    )

print("Column validation passed.\n")

for index, row in df.iterrows():

    try:

        account_name = str(
            row["account"]
        ).upper()

        with Session(engine) as session:

            account = session.query(Account).filter(
                Account.broker == account_name
            ).first()

            if not account:

                raise Exception(
                    f"Unknown account: {account_name}"
                )

            account_id = account.account_id

        trade_date = pd.to_datetime(
            row["trade_date"]
        ).date()

        print(
            f"Importing row {index + 2}: "
            f"{row['symbol']} "
            f"{row['action']} "
            f"{row['quantity']}"
        )

        add_transaction(
            account_id=account_id,
            trade_date=trade_date,
            symbol=str(row["symbol"]),
            action=str(row["action"]),
            quantity=float(row["quantity"]),
            trade_currency=str(row["trade_currency"]),
            trade_price=float(row["trade_price"]),
            fees=(
                0
                if pd.isna(row["fees"])
                else float(row["fees"])
            ),
            fx_rate_to_gbp=(
                1.0
                if pd.isna(row["fx_rate_to_gbp"])
                else float(row["fx_rate_to_gbp"])
            ),
            notes=str(row["notes"])
        )

    except Exception as e:

        print(
            f"Error processing row {index + 2}: {e}"
        )

print("\nImport complete.\n")