import pandas as pd

from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)

from app.engine.macro_regime_engine import (
    build_macro_regime
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from src.mappers.recommendation_mapper import (
    RecommendationMapper,
)

from app.engine.capital_engine import (
    build_capital_state
)

# -----------------------------------
# BUILD POSITION SIZING
# -----------------------------------

def build_position_sizing(
    market_context,
    portfolio_value,
    risk_intelligence_df
):
    capital_state = (
        build_capital_state()
    )

    deployable_capital = (
        capital_state[
            "deployable_capital"
        ]
    )

    capital_status = (
        capital_state[
            "capital_status"
        ]
    )

    df = build_buy_recommendations(
        market_context
    )

    # -----------------------------------
    # LOAD RISK DATA
    # -----------------------------------

    portfolio_risk_df = (

        build_portfolio_risk(
            market_context
        )
    )

    portfolio_risk_lookup = (

        portfolio_risk_df.set_index(

            "symbol"
        )
    )

    risk_lookup = (

        risk_intelligence_df.set_index(

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

    # -----------------------------------
    # BUILD POSITIONS
    # -----------------------------------

    for _, row in df.iterrows():

        recommendation = (
            RecommendationMapper
            .from_dataframe_row(row)
        )

        allocation_score = (

            recommendation.ai_score

            *

            recommendation.portfolio_fit_score
            
        )

        # -----------------------------------
        # CONVICTION
        # -----------------------------------

        if recommendation.rating == "STRONG_BUY":

            multiplier = 1.0

        elif recommendation.rating == "BUY":

            multiplier = 0.7

        elif recommendation.rating == "WATCH":

            multiplier = 0.4

        else:

            multiplier = 0.1

        # -----------------------------------
        # MACRO
        # -----------------------------------

        if regime == "RISK_ON":

            macro_multiplier = 1.2

        elif regime == "RISK_OFF":

            macro_multiplier = 0.6

        else:

            macro_multiplier = 1.0

        multiplier *= macro_multiplier

        # -----------------------------------
        # BASE POSITION
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
        # RISK LOOKUPS
        # -----------------------------------

        risk_lookup = (

            risk_intelligence_df.set_index(

                "symbol"
            )
        )

        asset_risk_score = (

            risk_lookup.loc[
                row["symbol"],
                "asset_risk_score"
            ]

            if row["symbol"]
            in risk_lookup.index

            else 0.5
        )

        portfolio_risk = (

            portfolio_risk_lookup.loc[
                row["symbol"],
                "portfolio_risk"
            ]

            if row["symbol"]
                in portfolio_risk_lookup.index

            else 0
        )
        
        # -----------------------------------
        # FINAL ADJUSTMENT
        # -----------------------------------

        adjusted_pct = round(

            suggested_pct

            *

            (1 - asset_risk_score)

            *

            (1 - portfolio_risk),

            2
        )

        adjusted_pct = min(

            adjusted_pct,

            15
        )

        suggested_value = round(

            portfolio_value

            *

            (

                adjusted_pct / 100
            ),

            2
        )
        
        if adjusted_pct <= 0:

            continue

        sizing_rows.append({

            "symbol":
                row["symbol"],

            "rating":
                row["rating"],

            "ai_score":
                row["ai_score"],

            "asset_risk_score":
                asset_risk_score,

            "portfolio_risk":
                portfolio_risk,

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

            "macro_regime":
                regime,

            "macro_multiplier":
                round(
                    macro_multiplier,
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