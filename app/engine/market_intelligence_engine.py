import pandas as pd

from app.services.technical_indicator_service import (
    get_technical_indicators
)

# -----------------------------------
# BUILD MARKET INTELLIGENCE
# -----------------------------------

def build_market_intelligence(

    symbols
):

    rows = []

    for symbol in symbols:

        data = get_technical_indicators(
            symbol
        )

        if not data:

            continue

        # -----------------------------------
        # MOMENTUM SCORE
        # -----------------------------------

        momentum_score = 1 if (

            data[
                "bullish_trend"
            ]

        ) else 0

        # -----------------------------------
        # RSI SCORE
        # LOWER RSI = BETTER ENTRY
        # -----------------------------------

        rsi_score = 1 - (
            data["rsi"] / 100
        )

        # -----------------------------------
        # AI SCORE
        # -----------------------------------

        ai_score = round(

            (

                momentum_score * 0.6

                +

                rsi_score * 0.4
            ),

            4
        )

        # -----------------------------------
        # WATCHLIST RATING
        # -----------------------------------

        if ai_score >= 0.8:

            rating = "STRONG"

        elif ai_score >= 0.6:

            rating = "BUY"

        elif ai_score >= 0.4:

            rating = "WATCH"

        else:

            rating = "AVOID"

        rows.append({

            "symbol":
                symbol,

            "price":
                data["price"],

            "ma50":
                data["ma50"],

            "ma200":
                data["ma200"],

            "rsi":
                data["rsi"],

            "bullish_trend":
                data["bullish_trend"],

            "momentum_score":
                momentum_score,

            "rsi_score":
                round(rsi_score, 4),

            "ai_score":
                ai_score,

            "rating":
                rating
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(

        by="ai_score",

        ascending=False
    )

    return df