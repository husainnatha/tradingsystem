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
# BUILD INVENTORY STATE
# -----------------------------------

def build_inventory_state():

    session = SessionLocal()

    results = get_section_104_pool()

    inventory_rows = []

    # -----------------------------------
    # LOAD BUY TRANSACTIONS
    # -----------------------------------

    buy_transactions = (

        session.query(Transaction)

        .filter(
            Transaction.action == "BUY"
        )

        .all()
    )

    for tx in buy_transactions:

        inventory_rows.append({

            "transaction_id":
                tx.transaction_id,

            "symbol":
                tx.symbol,

            "trade_date":
                tx.trade_date,

            "original_quantity":
                tx.quantity,

            "matched_quantity":
                0,

            "remaining_quantity":
                tx.quantity,

            "trade_price":
                tx.trade_price,

            "fx_rate_to_gbp":
                tx.fx_rate_to_gbp,

            "cost_gbp":
                round(

                    tx.quantity *

                    tx.trade_price *

                    tx.fx_rate_to_gbp,

                    2
                ),

            "match_rule":
                None
        })

    inventory_df = pd.DataFrame(
        inventory_rows
    )

        # -----------------------------------
    # APPLY SAME-DAY MATCHES
    # -----------------------------------

    same_day_matches = (

        results[
            "same_day_results"
        ][
            "matches"
        ]
    )

    for match in same_day_matches:

        buy_transaction_id = match[
            "buy_transaction_id"
        ]

        matched_quantity = match[
            "matched_quantity"
        ]

        mask = (

            inventory_df[
                "transaction_id"
            ]

            ==

            buy_transaction_id
        )

        inventory_df.loc[

            mask,

            "matched_quantity"

        ] += matched_quantity

        inventory_df.loc[

            mask,

            "remaining_quantity"

        ] -= matched_quantity

        inventory_df.loc[

            mask,

            "match_rule"

        ] = "SAME_DAY"

    # -----------------------------------
    # APPLY THIRTY-DAY MATCHES
    # -----------------------------------

    thirty_day_matches = (

        results[
            "thirty_day_matches"
        ]
    )

    for match in thirty_day_matches:

        buy_transaction_id = match[
            "buy_transaction_id"
        ]

        matched_quantity = match[
            "matched_quantity"
        ]

        mask = (

            inventory_df[
                "transaction_id"
            ]

            ==

            buy_transaction_id
        )

        inventory_df.loc[

            mask,

            "matched_quantity"

        ] += matched_quantity

        inventory_df.loc[

            mask,

            "remaining_quantity"

        ] -= matched_quantity

        inventory_df.loc[

            mask,

            "match_rule"

        ] = "THIRTY_DAY"

    # -----------------------------------
    # APPLY SECTION 104 DISPOSALS
    # -----------------------------------

    s104_disposals = (

        results[
            "section_104_disposals"
        ]
    )

    for disposal in s104_disposals:

        symbol = disposal[
            "symbol"
        ]

        matched_quantity = disposal[
            "matched_quantity"
        ]

        # -----------------------------------
        # FIND AVAILABLE INVENTORY
        # -----------------------------------

        available_rows = (

            inventory_df[

                (
                    inventory_df[
                        "symbol"
                    ] == symbol
                )

                &

                (
                    inventory_df[
                        "remaining_quantity"
                    ] > 0
                )
            ]

            .sort_values(
                by="trade_date"
            )
        )

        qty_remaining_to_match = (
            matched_quantity
        )

        # -----------------------------------
        # CONSUME INVENTORY
        # -----------------------------------

        for idx, row in available_rows.iterrows():

            if qty_remaining_to_match <= 0:

                break

            available_qty = row[
                "remaining_quantity"
            ]

            consume_qty = min(

                available_qty,

                qty_remaining_to_match
            )

            inventory_df.loc[

                idx,

                "matched_quantity"

            ] += consume_qty

            inventory_df.loc[

                idx,

                "remaining_quantity"

            ] -= consume_qty

            inventory_df.loc[

                idx,

                "match_rule"

            ] = "SECTION_104"

            qty_remaining_to_match -= (
                consume_qty
            )

    session.close()

    return inventory_df