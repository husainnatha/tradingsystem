import pandas as pd

from app.engine.ranking_engine import (
    build_ranked_inventory
)

# -----------------------------------
# OPTIMISE SALE STRATEGY
# -----------------------------------

def optimise_sale_strategy(

    target_cash,
    strategy="growth"
):

    inventory_df = build_ranked_inventory(
    strategy=strategy
)

    # -----------------------------------
    # FILTER AVAILABLE INVENTORY
    # -----------------------------------

    inventory_df = inventory_df[

        inventory_df[
            "remaining_quantity"
        ] > 0
    ]

    # -----------------------------------
    # SORT BEST AI CANDIDATES
    # -----------------------------------

    inventory_df = inventory_df.sort_values(

        by="ai_score",

        ascending=False
    )

    # -----------------------------------
    # SORT LOWEST GAIN FIRST
    # -----------------------------------

    inventory_df = inventory_df.sort_values(

        by="gain_per_share",

        ascending=True
    )

    # -----------------------------------
    # BUILD STRATEGY
    # -----------------------------------

    cash_remaining = target_cash

    recommendations = []

    for _, row in inventory_df.iterrows():

        if cash_remaining <= 0:

            break

        current_price = row[
            "current_price"
        ]

        remaining_qty = row[
            "remaining_quantity"
        ]

        max_position_value = (

            current_price *

            remaining_qty
        )

        # -----------------------------------
        # DETERMINE SALE SIZE
        # -----------------------------------

        if max_position_value <= cash_remaining:

            sell_qty = remaining_qty

        else:

            sell_qty = (

                cash_remaining /

                current_price
            )

        estimated_proceeds = (
            sell_qty *
            current_price
        )

        estimated_cost = (

            sell_qty *

            (
                row[
                    "remaining_cost_gbp"
                ]

                /

                remaining_qty
            )
        )

        estimated_gain = (
            estimated_proceeds
            -
            estimated_cost
        )

        recommendations.append({

            "symbol":
                row["symbol"],

            "sell_quantity":
                round(sell_qty, 2),

            "estimated_proceeds":
                round(
                    estimated_proceeds,
                    2
                ),

            "estimated_gain":
                round(
                    estimated_gain,
                    2
                ),

            "gain_per_share":
                round(
                    row[
                        "gain_per_share"
                    ],
                    2
                ),
            
            "ai_score":
                round(
                    row["ai_score"],
                    4
                ),

            "tax_score":
                round(
                    row[
                        "tax_efficiency_score"
                    ],
                    4
                ),

            "risk_score":
                round(
                    row[
                        "position_risk_score"
                    ],
                    4
                ),

            "holding_score":
                round(
                    row[
                        "holding_period_score"
                    ],
                    4
                )
        })

        cash_remaining -= (
            estimated_proceeds
        )

    return pd.DataFrame(
        recommendations
    )