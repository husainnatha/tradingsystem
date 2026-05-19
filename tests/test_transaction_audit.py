from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import engine
from app.database.models import Transaction

with Session(engine) as session:

    transactions = session.scalars(

        select(Transaction).order_by(
            Transaction.trade_date
        )

    ).all()

    print("\nTransaction Audit:\n")

    for tx in transactions:

        print(
            f"{tx.trade_date} | "
            f"{tx.symbol} | "
            f"{tx.action} | "
            f"Qty={tx.quantity} | "
            f"Price={tx.trade_price} | "
            f"FX={tx.fx_rate_to_gbp} | "
            f"GBP={tx.gbp_net_amount:.2f}"
        )