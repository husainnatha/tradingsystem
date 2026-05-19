import hashlib

from sqlalchemy.orm import Session

from app.database.db import engine
from app.database.models import Transaction


def add_transaction(
    account_id,
    trade_date,
    symbol,
    action,
    quantity,
    trade_currency,
    trade_price,
    fees,
    fx_rate_to_gbp,
    notes=""
):

    gbp_net_amount = (
        (quantity * trade_price) + fees
    ) * fx_rate_to_gbp

    hash_input = (
    f"{account_id}|"
    f"{trade_date}|"
    f"{symbol}|"
    f"{action}|"
    f"{quantity}|"
    f"{trade_price}"
)

    transaction_hash = hashlib.sha256(
        hash_input.encode()
    ).hexdigest()

    with Session(engine) as session:
        
        existing = session.query(Transaction).filter_by(
            transaction_hash=transaction_hash
        ).first()

        if existing:

            print(
                f"Duplicate transaction skipped: "
                f"{symbol} {trade_date}"
            )

            return

        transaction = Transaction(
            account_id=account_id,
            transaction_hash=transaction_hash,
            trade_date=trade_date,
            symbol=symbol.upper(),
            action=action.upper(),
            quantity=quantity,
            trade_currency=trade_currency.upper(),
            trade_price=trade_price,
            fees=fees,
            fx_rate_to_gbp=fx_rate_to_gbp,
            gbp_net_amount=gbp_net_amount,
            notes=notes
        )

        session.add(transaction)

        session.commit()

        print(
            f"Transaction added: "
            f"{action} {quantity} {symbol}"
        )