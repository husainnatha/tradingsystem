import pandas as pd

from app.services.technical_indicator_service import (
    get_technical_indicators
)

from app.engine.sector_intelligence import (
    build_sector_exposure
)

from app.config.sector_map import (
    get_sector
)

from app.engine.macro_regime_engine import (
    build_macro_regime
)

# -----------------------------------
# BUILD MARKET INTELLIGENCE
# -----------------------------------

def build_market_intelligence(

    symbols
):
        # -----------------------------------
    # LOAD MACRO REGIME
    # -----------------------------------

    macro = build_macro_regime()

    regime = macro[
        "regime"
    ]

    # -----------------------------------
    # LOAD PORTFOLIO SECTOR EXPOSURE
    # -----------------------------------

    sector_df = build_sector_exposure()

    sector_lookup = dict(

        zip(

            sector_df[
                "sector"
            ],

            sector_df[
                "exposure_pct"
            ]
        )
    )

    rows = []

    # -----------------------------------
    # PROCESS WATCHLIST
    # -----------------------------------

    for symbol in symbols:

        sector = get_sector(
            symbol
        )

        current_exposure = sector_lookup.get(

            sector,

            0
        )

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
        # PORTFOLIO FIT SCORE
        # LOWER EXPOSURE = BETTER FIT
        # -----------------------------------

        portfolio_fit_score = 1 - min(

            current_exposure / 100,

            1
        )

        # -----------------------------------
        # MACRO SCORE
        # -----------------------------------

        macro_score = 0.5

        if regime == "RISK_ON":

            macro_score = (

                1

                if momentum_score

                else 0.25
            )

        elif regime == "RISK_OFF":

            macro_score = (

                0.2

                if momentum_score

                else 0.8
            )

        # -----------------------------------
        # AI SCORE
        # -----------------------------------

        ai_score = round(

            (

                momentum_score * 0.30

                +

                rsi_score * 0.20

                +

                portfolio_fit_score * 0.30

                +

                macro_score * 0.20

            ),

            4
        )

        # -----------------------------------
        # RATING
        # -----------------------------------

        if (

            ai_score >= 0.8

            and

            portfolio_fit_score >= 0.6
        ):

            rating = "STRONG"

        elif ai_score >= 0.6:

            rating = "BUY"

        elif ai_score >= 0.4:

            rating = "WATCH"

        else:

            rating = "AVOID"

        # -----------------------------------
        # WATCHLIST RATING
        # -----------------------------------

        if (
            ai_score >= 0.8

            and

            portfolio_fit_score >= 0.6
        ):

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
                rating,
            
            "sector":
                sector,

            "portfolio_exposure":
                round(
                    current_exposure,
                    2
                ),

            "portfolio_fit_score":
                round(
                    portfolio_fit_score,
                    4
                ),
            
            "macro_regime":
                regime,

            "macro_score":
                macro_score
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(

        by="ai_score",

        ascending=False
    )

    sector_df = build_sector_exposure()

    sector_lookup = dict(

        zip(

            sector_df[
                "sector"
            ],

            sector_df[
                "exposure_pct"
            ]
        )
    )

    return df