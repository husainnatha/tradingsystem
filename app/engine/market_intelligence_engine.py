import pandas as pd

from app.engine.sector_intelligence import (
    build_sector_exposure
)

from app.config.sector_map import (
    get_sector
)

from app.engine.macro_regime_engine import (
    build_macro_regime
)

from app.config.macro_sector_preferences import (
    get_sector_bias
)

from app.engine.correlation_engine import (
    build_correlation_engine
)

# -----------------------------------
# BUILD MARKET INTELLIGENCE
# -----------------------------------

def build_market_intelligence(
    market_context
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

    # -----------------------------------
    # LOAD CORRELATION DATA
    # -----------------------------------

    correlation_df = (

        build_correlation_engine()
    )

    correlation_lookup = (

        correlation_df

        .set_index(

            "symbol"
        )[
            "diversification_score"
        ]

        .to_dict()
    )

    rows = []

    # -----------------------------------
    # PROCESS WATCHLIST
    # -----------------------------------

    for symbol, df in (
        market_context
        .get_all()
        .items()
    ):
        sector = get_sector(
            symbol
        )

        current_exposure = sector_lookup.get(

            sector,

            0
        )

        close = (
            df["Close"]
            .squeeze()
        )

        latest = df.iloc[-1]

        price = float(
            close.iloc[-1]
        )

        ma50 = float(
            latest["MA50"].squeeze()
        )

        ma200 = float(
            latest["MA200"].squeeze()
        )

        rsi = float(
            latest["RSI"].squeeze()
        )

        bullish_trend = (
            ma50 > ma200
        )

        data = {

            "price":
                price,

            "ma50":
                ma50,

            "ma200":
                ma200,

            "rsi":
                rsi,

            "bullish_trend":
                bullish_trend
        }

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
        # SECTOR MACRO BIAS
        # -----------------------------------

        sector_bias = get_sector_bias(

            regime,

            sector
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
        # TECHNICAL SCORE
        # -----------------------------------

        technical_score = round(

            (

                momentum_score

                +

                rsi_score

            )

            / 2,

            4
        )

        # -----------------------------------
        # AI SCORE
        # -----------------------------------

        # -----------------------------------
        # CORRELATION ADJUSTMENT
        # -----------------------------------

        diversification_score = (

            correlation_lookup.get(

                symbol,

                0.5
            )
        )

        ai_score = round(

            technical_score

            * 0.30

            +

            macro_score

            * 0.20

            +

            portfolio_fit_score

            * 0.15

            +

            diversification_score

            * 0.15

            +

            sector_bias

            * 0.20,

            4
        )

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
            
            "technical_score":
                technical_score,

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
                round(
                    macro_score,
                    4
                ),

            "sector_bias":
                round(
                    sector_bias,
                    4
                ),

            "diversification_score":
                round(
                    diversification_score,
                    4
                )
        })

    df = pd.DataFrame(rows)

    df = df.sort_values(

        by="ai_score",

        ascending=False
    )

    return df