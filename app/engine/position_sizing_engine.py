import pandas as pd

from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)

from app.engine.macro_regime_engine import (
    build_macro_regime
)

from app.engine.risk_engine import (
    build_risk_engine
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

    risk_df = (

    build_risk_engine()
    )

    if risk_df.empty:

        raise Exception(

            "Risk engine returned no data"
        )

    risk_lookup = (

        risk_df.set_index(

            "symbol"
        )
    )

    # -----------------------------------
    # LOAD MACRO REGIME
    # -----------------------------------

    macro = build_macro_regime()

    regime = macro[
        "regime"
    ]

    sizing_rows = []

    risk_df = (

    build_risk_engine()
)

    # Safety check

    if risk_df.empty:

        raise Exception(

            "Risk engine returned no data"
        )

    risk_lookup = (

        risk_df.set_index(
            "symbol"
        )
    )

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
        # BASE CONVICTION MULTIPLIER
        # -----------------------------------

        if row["rating"] == "STRONG_BUY":

            multiplier = 1.0

        elif row["rating"] == "BUY":

            multiplier = 0.7

        elif row["rating"] == "WATCH":

            multiplier = 0.4

        else:

            multiplier = 0.1

        # -----------------------------------
        # MACRO REGIME ADJUSTMENT
        # -----------------------------------

        if regime == "RISK_ON":

            macro_multiplier = 1.2

        elif regime == "RISK_OFF":

            macro_multiplier = 0.6

        else:

            macro_multiplier = 1.0

        multiplier *= macro_multiplier

        # -----------------------------------
        # CALCULATE ALLOCATION %
        # -----------------------------------

        suggested_pct = round(

            allocation_score

            *

            multiplier

            *

            10,

            2
        )

        # -----------------------------------

        risk_score = (

            risk_lookup.loc[
                row["symbol"],
                "risk_score"
            ]

            if row["symbol"] in risk_lookup.index

            else 0.5
        )

        # -----------------------------------
        # RISK ADJUSTMENT
        # -----------------------------------

        adjusted_pct = round(

            suggested_pct

            * (1 - risk_score),

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

            portfolio_value

            *

            (

                adjusted_pct / 100
            ),

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

        sizing_rows.append({

            "symbol":
                row["symbol"],
            
            "suggested_pct":
                suggested_pct,
            
            "risk_score":
                risk_score,

            "adjusted_pct":
                adjusted_pct,

            "rating":
                row["rating"],

            "ai_score":
                row["ai_score"],

            "suggested_allocation_pct":
                adjusted_pct,

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
                row["explanation"],

                        "macro_regime":
                regime,

            "macro_multiplier":
                round(
                    macro_multiplier,
                    2
                )
        })

    result_df = pd.DataFrame(
        sizing_rows
    )

    result_df = result_df.sort_values(

        by="suggested_allocation_pct",

        ascending=False
    )

    return result_df