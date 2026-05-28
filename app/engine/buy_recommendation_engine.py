import pandas as pd

from app.engine.market_intelligence_engine import (
    build_market_intelligence
)

# -----------------------------------
# BUILD BUY RECOMMENDATIONS
# -----------------------------------

def build_buy_recommendations(
    market_context
):

    df = build_market_intelligence(
        market_context
    )

    recommendations = []

    for _, row in df.iterrows():

        # -----------------------------------
        # RECOMMENDATION LOGIC
        # -----------------------------------

        if row[
            "ai_score"
        ] >= 0.8:

            recommendation = "STRONG_BUY"

        elif row[
            "ai_score"
        ] >= 0.6:

            recommendation = "BUY"

        elif row[
            "ai_score"
        ] >= 0.4:

            recommendation = "WATCH"

        else:

            recommendation = "AVOID"

        # -----------------------------------
        # EXPLANATION
        # -----------------------------------

        explanation_parts = []

        if row[
            "bullish_trend"
        ]:

            explanation_parts.append(

                "bullish trend"
            )

        if row[
            "rsi"
        ] < 40:

            explanation_parts.append(

                "potentially oversold"
            )

        if row[
            "portfolio_fit_score"
        ] >= 0.7:

            explanation_parts.append(

                "improves diversification"
            )

        elif row[
            "portfolio_fit_score"
        ] <= 0.4:

            explanation_parts.append(

                "increases concentration risk"
            )

        explanation = (

            ", ".join(
                explanation_parts
            )

            if explanation_parts

            else

            "balanced opportunity profile"
        )

        recommendations.append({

            "symbol":
                row["symbol"],

            "sector":
                row["sector"],

            "price":
                row["price"],

            "ai_score":
                row["ai_score"],
            
            "ma50": row["ma50"],
            "ma200": row["ma200"],
            "bullish_trend": row["bullish_trend"],

            "rating":
                recommendation,

            "bullish_trend":
                row[
                    "bullish_trend"
                ],

            "rsi":
                row["rsi"],

            "portfolio_fit_score":
                row[
                    "portfolio_fit_score"
                ],

            "explanation":
                explanation
        })

    result_df = pd.DataFrame(
        recommendations
    )

    result_df = result_df.sort_values(

        by="ai_score",

        ascending=False
    )

    return result_df