import pandas as pd

from app.engine.inventory_engine import (
    build_inventory_state
)

from app.engine.correlation_engine import (
    build_correlation_engine
)

def build_portfolio_risk(
    market_context
):

    inventory = (

        build_inventory_state()
    )

    # -----------------------------------
    # AGGREGATE TO HOLDING LEVEL
    # -----------------------------------

    inventory = (

        inventory

        .groupby(

            "symbol",

            as_index=False
        )

        .agg({

            "market_value_gbp":
                "sum"
        })

        .query(

            "market_value_gbp > 0"
        )
    )

    # print(
    #         "\nINVENTORY:\n"
    #     )

    # print(
    #         inventory.to_string()
    #     )

    correlation = (

        build_correlation_engine(
            market_context
        )
    )

    rows = []

    total_value = (

        inventory[
            "market_value_gbp"
        ].sum()
    )

    for _, row in inventory.iterrows():

        concentration = round(

        row["market_value_gbp"]

        / total_value,

        4
    )

        corr = (

            correlation.loc[

                correlation[
                    "symbol"
                ]

                == row[
                    "symbol"
                ],

                "avg_correlation"
            ]
        )

        avg_corr = (

            corr.iloc[0]

            if len(corr)

            else 0
        )

        portfolio_risk = min(

            max(

                round(

                    (

                        concentration

                        + abs(
                            avg_corr
                        )

                    ) / 2,

                    4
                ),

                0
            ),

            1
        )

        inventory = (

            inventory[

                inventory[
                    "market_value_gbp"
                ] > 0
            ]
        )

        rows.append({

            "symbol":
                row["symbol"],

            "concentration":
                concentration,

            "portfolio_risk":
                portfolio_risk
        })

    return pd.DataFrame(
        rows
    )