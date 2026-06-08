import hashlib

from sqlalchemy.orm import Session

from app.database.db import engine

from app.database.models import (
    Transaction
)

# -----------------------------------
# ADD TRANSACTION
# -----------------------------------


def add_transaction(

    trade_date,

    account,

    symbol,

    action,

    quantity,

    trade_currency,

    trade_price,

    fees,

    fx_rate_to_gbp,

    notes=""
):

    # -----------------------------------
    # CALCULATE GBP NET AMOUNT
    # -----------------------------------

    gbp_net_amount = (

        quantity
        * trade_price
        * fx_rate_to_gbp

    ) + fees

    # -----------------------------------
    # CREATE TRANSACTION HASH
    # -----------------------------------

    transaction_string = (

        f"{trade_date}|"

        f"{account}|"

        f"{symbol}|"

        f"{action}|"

        f"{quantity}|"

        f"{trade_price}"
    )

    transaction_hash = hashlib.sha256(

        transaction_string.encode()

    ).hexdigest()

    # -----------------------------------
    # INSERT TRANSACTION
    # -----------------------------------

    with Session(engine) as session:

        existing = session.query(
            Transaction
        ).filter(

            Transaction.transaction_hash
            ==
            transaction_hash

        ).first()

        if existing:

            print(
                f"Duplicate skipped: "
                f"{symbol}"
            )

            return

        transaction = Transaction(

            transaction_hash=
                transaction_hash,

            trade_date=
                trade_date,

            account=
                account,

            symbol=
                symbol,

            action=
                action,

            quantity=
                quantity,

            trade_currency=
                trade_currency,

            trade_price=
                trade_price,

            fees=
                fees,

            fx_rate_to_gbp=
                fx_rate_to_gbp,

            gbp_net_amount=
                gbp_net_amount,

            notes=
                notes
        )

        session.add(
            transaction
        )

        session.commit()

        print(
            f"Inserted: "
            f"{symbol}"
        )