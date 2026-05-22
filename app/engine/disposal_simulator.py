import pandas as pd

from app.engine.inventory_engine import (
    build_inventory_state
)

from app.config.tax_config import (
    UK_TAX_CONFIG
)

# -----------------------------------
# SIMULATE DISPOSAL
# -----------------------------------

def simulate_sale(

    symbol,
    quantity,
    sell_price,
    tax_year="2025/26"
):

    inventory_df = build_inventory_state()

    # -----------------------------------
    # FILTER AVAILABLE INVENTORY
    # -----------------------------------

    symbol_inventory = inventory_df[

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

    total_available = symbol_inventory[
        "remaining_quantity"
    ].sum()

    # -----------------------------------
    # VALIDATE INVENTORY
    # -----------------------------------

    if quantity > total_available:

        raise Exception(

            f"Not enough inventory. "

            f"Available={total_available}"
        )

    # -----------------------------------
    # SIMULATE SECTION 104 CONSUMPTION
    # -----------------------------------

    qty_remaining_to_sell = quantity

    allowable_cost = 0

    consumption_rows = []

    for _, row in symbol_inventory.iterrows():

        if qty_remaining_to_sell <= 0:

            break

        available_qty = row[
            "remaining_quantity"
        ]

        consume_qty = min(

            available_qty,

            qty_remaining_to_sell
        )

        proportional_cost = (

            row[
                "remaining_cost_gbp"
            ]

            /

            row[
                "remaining_quantity"
            ]
        )

        consumed_cost = (

            consume_qty *

            proportional_cost
        )

        allowable_cost += (
            consumed_cost
        )

        consumption_rows.append({

            "transaction_id":
                row["transaction_id"],

            "consume_qty":
                consume_qty,

            "cost_per_share":
                round(
                    proportional_cost,
                    4
                ),

            "consumed_cost":
                round(
                    consumed_cost,
                    2
                )
        })

        qty_remaining_to_sell -= (
            consume_qty
        )

    # -----------------------------------
    # CALCULATE DISPOSAL
    # -----------------------------------

    proceeds = quantity * sell_price

    estimated_gain = (
        proceeds - allowable_cost
    )

    config = UK_TAX_CONFIG[
        tax_year
    ]

    allowance = config[
        "cgt_allowance"
    ]

    taxable_gain = max(

        0,

        estimated_gain - allowance
    )

    estimated_cgt = (

        taxable_gain *

        config[
            "higher_cgt_rate"
        ]
    )

    # -----------------------------------
    # RETURN RESULT
    # -----------------------------------

    return {

        "symbol":
            symbol,

        "quantity":
            quantity,

        "sell_price":
            sell_price,

        "proceeds":
            round(proceeds, 2),

        "allowable_cost":
            round(allowable_cost, 2),

        "estimated_gain":
            round(estimated_gain, 2),

        "taxable_gain":
            round(taxable_gain, 2),

        "estimated_cgt":
            round(estimated_cgt, 2),

        "consumption_rows":
            consumption_rows
    }