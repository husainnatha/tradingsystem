import pandas as pd

from app.database.db import (
    SessionLocal
)

from app.database.models import (
    Transaction
)

from app.engine.matching_engine import (
    get_section_104_pool
)

# -----------------------------------
# BUILD MATCHING LEDGER
# -----------------------------------

def build_matching_ledger():

    session = SessionLocal()

    results = get_section_104_pool()

    rows = []

    # -----------------------------------
    # SAME-DAY MATCHES
    # -----------------------------------

    same_day_matches = (

        results[
            "same_day_results"
        ][
            "matches"
        ]
    )

    for match in same_day_matches:

        sell_tx = session.get(

            Transaction,

            match[
                "sell_transaction_id"
            ]
        )

        buy_tx = session.get(

            Transaction,

            match[
                "buy_transaction_id"
            ]
        )

        qty = match[
            "matched_quantity"
        ]

        proceeds = (

            qty *

            sell_tx.trade_price *

            sell_tx.fx_rate_to_gbp
        )

        cost_basis = (

            qty *

            buy_tx.trade_price *

            buy_tx.fx_rate_to_gbp
        )

        gain_loss = (
            proceeds - cost_basis
        )

        rows.append({

            "rule":
                "SAME_DAY",

            "symbol":
                sell_tx.symbol,

            "sell_date":
                sell_tx.trade_date,

            "buy_date":
                buy_tx.trade_date,

            "sell_transaction_id":
                sell_tx.transaction_id,

            "buy_transaction_id":
                buy_tx.transaction_id,

            "original_buy_quantity":
                buy_tx.quantity,

            "matched_quantity":
                qty,

            "remaining_quantity":
                round(
                    buy_tx.quantity - qty,
                    2
                ),

            "proceeds_gbp":
                round(proceeds, 2),

            "matched_cost_gbp":
                round(cost_basis, 2),

            "gain_loss_gbp":
                round(gain_loss, 2),
            
            "buy_price":
                buy_tx.trade_price,

            "sell_price":
                sell_tx.trade_price,

            "buy_fx_rate":
                buy_tx.fx_rate_to_gbp,

            "sell_fx_rate":
                sell_tx.fx_rate_to_gbp,

            "buy_price_gbp":
                round(
                    buy_tx.trade_price *
                    buy_tx.fx_rate_to_gbp,
                    4
                ),

            "sell_price_gbp":
                round(
                    sell_tx.trade_price *
                    sell_tx.fx_rate_to_gbp,
                    4
                ),

            "gain_loss_per_share_gbp":
                round(
                    gain_loss / qty,
                    4
                ),

            "holding_period_days":
                (
                    sell_tx.trade_date
                    - buy_tx.trade_date
                ).days
        })

    # -----------------------------------
    # THIRTY-DAY MATCHES
    # -----------------------------------

    thirty_day_matches = (
        results[
            "thirty_day_matches"
        ]
    )

    for match in thirty_day_matches:

        sell_tx = session.get(

            Transaction,

            match[
                "sell_transaction_id"
            ]
        )

        buy_tx = session.get(

            Transaction,

            match[
                "buy_transaction_id"
            ]
        )

        qty = match[
            "matched_quantity"
        ]

        proceeds = (

            qty *

            sell_tx.trade_price *

            sell_tx.fx_rate_to_gbp
        )

        cost_basis = (

            qty *

            buy_tx.trade_price *

            buy_tx.fx_rate_to_gbp
        )

        gain_loss = (
            proceeds - cost_basis
        )

        rows.append({

            "rule":
                "THIRTY_DAY",

            "symbol":
                sell_tx.symbol,

            "sell_date":
                sell_tx.trade_date,

            "buy_date":
                buy_tx.trade_date,

            "sell_transaction_id":
                sell_tx.transaction_id,

            "buy_transaction_id":
                buy_tx.transaction_id,

            "original_buy_quantity":
                buy_tx.quantity,

            "matched_quantity":
                qty,

            "remaining_quantity":
                round(
                    buy_tx.quantity - qty,
                    2
                ),

            "proceeds_gbp":
                round(proceeds, 2),

            "matched_cost_gbp":
                round(cost_basis, 2),

            "gain_loss_gbp":
                round(gain_loss, 2),
            
            "buy_price":
                buy_tx.trade_price,

            "sell_price":
                sell_tx.trade_price,

            "buy_fx_rate":
                buy_tx.fx_rate_to_gbp,

            "sell_fx_rate":
                sell_tx.fx_rate_to_gbp,

            "buy_price_gbp":
                round(
                    buy_tx.trade_price *
                    buy_tx.fx_rate_to_gbp,
                    4
                ),

            "sell_price_gbp":
                round(
                    sell_tx.trade_price *
                    sell_tx.fx_rate_to_gbp,
                    4
                ),

            "gain_loss_per_share_gbp":
                round(
                    gain_loss / qty,
                    4
                ),

            "holding_period_days":
                (
                    sell_tx.trade_date
                    - buy_tx.trade_date
                ).days
        })

    session.close()

    return pd.DataFrame(rows)