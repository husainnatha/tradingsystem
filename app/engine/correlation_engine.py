import pandas as pd
import yfinance as yf

from app.config.watchlist import (
    WATCHLIST
)

# -----------------------------------
# CACHE
# -----------------------------------

_cached_correlation_df = None


# -----------------------------------
# BUILD CORRELATION ENGINE
# -----------------------------------

def build_correlation_engine(

    symbols=WATCHLIST
):

    global _cached_correlation_df

    # -----------------------------------
    # USE CACHE
    # -----------------------------------

    if _cached_correlation_df is not None:

        return _cached_correlation_df

    print(

        "\nLoading price history once...\n"
    )

    prices = pd.DataFrame()

    # -----------------------------------
    # DOWNLOAD DATA
    # -----------------------------------

    for symbol in symbols:

        try:

            data = yf.download(

                symbol,

                period="6mo",

                progress=False
            )

            prices[symbol] = (

                data[
                    "Close"
                ]
            )

        except Exception:

            print(
                f"Failed: {symbol}"
            )

    # -----------------------------------
    # DAILY RETURNS
    # -----------------------------------

    returns = (

        prices

        .pct_change()

        .dropna()
    )

    # -----------------------------------
    # CORRELATION MATRIX
    # -----------------------------------

    correlation = (

        returns

        .corr()
    )

    rows = []

    for symbol in correlation.columns:

        avg_corr = (

            correlation[
                symbol
            ]

            .drop(
                symbol
            )

            .mean()
        )

        diversification_score = round(

            (1 - avg_corr) / 2,

            4
        )

        rows.append({

            "symbol":
                symbol,

            "avg_correlation":
                round(
                    avg_corr,
                    4
                ),

            "diversification_score":
                diversification_score
        })

    result = pd.DataFrame(

        rows

    ).sort_values(

        by="diversification_score",

        ascending=False
    )

    # -----------------------------------
    # STORE CACHE
    # -----------------------------------

    _cached_correlation_df = result

    return result