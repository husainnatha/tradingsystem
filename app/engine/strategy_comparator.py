import pandas as pd

from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

# -----------------------------------
# COMPARE STRATEGIES
# -----------------------------------

def compare_strategies(

    required_sale_value=10000
):

    strategies = [

        "tax_saver",

        "growth",

        "risk_reduction"
    ]

    rows = []

    for strategy in strategies:

        df = optimise_sale_strategy(

            required_sale_value=10000,

            strategy=strategy
        )

        for _, row in df.iterrows():

            rows.append({

                "strategy":
                    strategy,

                "symbol":
                    row["symbol"],

                "sell_quantity":
                    row["sell_quantity"],

                "estimated_proceeds":
                    row[
                        "estimated_proceeds"
                    ],

                "estimated_gain":
                    row[
                        "estimated_gain"
                    ],

                "ai_score":
                    row["ai_score"]
            })

    comparison_df = pd.DataFrame(
        rows
    )

    return comparison_df