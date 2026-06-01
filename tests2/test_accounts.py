from sqlalchemy.orm import Session

from app.database.db import engine
from app.database.models import Account

accounts = [
    ("IBKR", "IBKR Main", "GBP"),
    ("IWEB", "iWeb Main", "GBP")
]

with Session(engine) as session:

    for broker, name, currency in accounts:

        existing = session.query(Account).filter_by(
            broker=broker
        ).first()

        if not existing:

            account = Account(
                broker=broker,
                account_name=name,
                currency=currency
            )

            session.add(account)

    session.commit()

print("Accounts setup complete.")