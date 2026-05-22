import pandas as pd

from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)

# -----------------------------------
# BUILD POSITION SIZING
# -----------------------------------

def build_position_sizing(

    watchlist,

    portfolio_value
):

    df = build_buy_recommendations(
        watchlist
    )

    sizing_rows = []

    for _, row in df.iterrows():

        # -----------------------------------
        # BASE ALLOCATION
        # -----------------------------------

        allocation_score = (

            row["ai_score"]

            *

            row[
                "portfolio_fit_score"
            ]
        )

        # -----------------------------------
        # RISK ADJUSTMENT
        # -----------------------------------

        if row["rating"] == "STRONG_BUY":

            multiplier = 1.0

        elif row["rating"] == "BUY":

            multiplier = 0.7

        elif row["rating"] == "WATCH":

            multiplier = 0.4

        else:

            multiplier = 0.1

        suggested_pct = round(

            allocation_score *

            multiplier *

            10,

            2
        )

        # -----------------------------------
        # CAP MAX POSITION
        # -----------------------------------

        suggested_pct = min(

            suggested_pct,

            15
        )

        # -----------------------------------
        # SUGGESTED CAPITAL
        # -----------------------------------

        suggested_value = round(

            portfolio_value *

            (

                suggested_pct / 100
            ),

            2
        )

        sizing_rows.append({

            "symbol":
                row["symbol"],

            "rating":
                row["rating"],

            "ai_score":
                row["ai_score"],

            "suggested_allocation_pct":
                suggested_pct,

            "suggested_position_value":
                suggested_value,

            "price":
                row["price"],

            "suggested_shares":

                round(

                    suggested_value

                    /

                    row["price"],

                    2
                ),

            "explanation":
                row["explanation"]
        })

    result_df = pd.DataFrame(
        sizing_rows
    )

    result_df = result_df.sort_values(

        by="suggested_allocation_pct",

        ascending=False
    )

    return result_df