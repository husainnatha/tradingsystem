from datetime import date

from sqlalchemy.orm import Session

from app.database.db import engine
from app.database.models import Account, Transaction

with Session(engine) as session:

    account = Account(
        broker="IBKR",
        account_name="Main Account",
        currency="GBP"
    )

    session.add(account)

    session.commit()

    transaction = Transaction(
        account_id=account.account_id,
        trade_date=date.today(),
        symbol="POET",
        action="BUY",
        quantity=10,
        trade_currency="USD",
        trade_price=5.25,
        fees=1.00,
        fx_rate_to_gbp=0.79,
        gbp_net_amount=42.29,
        notes="Test transaction"
    )

    session.add(transaction)

    session.commit()

    print("Test data inserted successfully.")