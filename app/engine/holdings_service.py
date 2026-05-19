from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database.db import engine
from app.database.models import Transaction


def calculate_holdings():

    with Session(engine) as session:

        transactions = session.scalars(

            select(Transaction).order_by(
                Transaction.trade_date,
                Transaction.transaction_id
            )

        ).all()

        holdings = {}

        for tx in transactions:

            symbol = tx.symbol

            if symbol not in holdings:

                holdings[symbol] = {
                    "quantity": 0,
                    "pool_cost": 0,
                    "avg_cost": 0,
                    "realised_pnl": 0
                }

            holding = holdings[symbol]

            if tx.action == "BUY":

                holding["quantity"] += tx.quantity

                holding["pool_cost"] += tx.gbp_net_amount

                holding["avg_cost"] = (
                    holding["pool_cost"]
                    / holding["quantity"]
                )

            elif tx.action == "SELL":

                if holding["quantity"] <= 0:

                    continue

                avg_cost = holding["avg_cost"]

                cost_removed = (
                    tx.quantity * avg_cost
                )

                proceeds = tx.gbp_net_amount

                realised_pnl = (
                    proceeds - cost_removed
                )

                holding["quantity"] -= tx.quantity

                holding["pool_cost"] -= cost_removed

                holding["realised_pnl"] += realised_pnl

                if holding["quantity"] > 0:

                    holding["avg_cost"] = (
                        holding["pool_cost"]
                        / holding["quantity"]
                    )

                else:

                    holding["avg_cost"] = 0

        return holdings