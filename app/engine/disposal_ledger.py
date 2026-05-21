from app.database.db import SessionLocal
from app.database.models import Transaction
import pandas as pd

from app.config.tax_config import (
    get_tax_year
)

from app.engine.matching_engine import (
    get_section_104_pool
)

def build_disposal_ledger():

    disposals = []

    session = SessionLocal()

    results = get_section_104_pool()

    ledger = []

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

        ledger.append({

            "symbol":
                sell_tx.symbol,

            "disposal_date":
                sell_tx.trade_date,
            
            "tax_year":
                get_tax_year(
                    sell_tx.trade_date
                ),

            "rule":
                "SAME_DAY",

            "quantity":
                qty,

            "proceeds_gbp":
                round(proceeds, 2),

            "cost_basis_gbp":
                round(cost_basis, 2),

            "gain_loss_gbp":
                round(gain_loss, 2)
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

        ledger.append({

            "symbol":
                sell_tx.symbol,

            "disposal_date":
                sell_tx.trade_date,
            
            "tax_year":
                get_tax_year(
                    sell_tx.trade_date
                ),

            "rule":
                "THIRTY_DAY",

            "quantity":
                qty,

            "proceeds_gbp":
                round(proceeds, 2),

            "cost_basis_gbp":
                round(cost_basis, 2),

            "gain_loss_gbp":
                round(gain_loss, 2)
        })

    # -----------------------------------
    # SECTION 104 DISPOSALS
    # -----------------------------------

    s104_disposals = (
        results[
            "section_104_disposals"
        ]
    )

    for disposal in s104_disposals:

        sell_tx = session.get(

            Transaction,

            disposal[
                "sell_transaction_id"
            ]
        )

        qty = disposal[
            "matched_quantity"
        ]

        proceeds = (

            qty *

            sell_tx.trade_price *

            sell_tx.fx_rate_to_gbp
        )

        cost_basis = disposal[
            "matched_cost"
        ]

        gain_loss = (
            proceeds - cost_basis
        )

        ledger.append({

            "symbol":
                sell_tx.symbol,

            "disposal_date":
                sell_tx.trade_date,

            "tax_year":
                get_tax_year(
                    sell_tx.trade_date
                ),

            "rule":
                "SECTION_104",

            "quantity":
                qty,

            "proceeds_gbp":
                round(proceeds, 2),

            "cost_basis_gbp":
                round(cost_basis, 2),

            "gain_loss_gbp":
                round(gain_loss, 2)
        })

    session.close()

    disposals_df = pd.DataFrame(
        ledger
    )

    return disposals_df