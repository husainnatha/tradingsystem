import pandas as pd
import yfinance as yf

from app.config.watchlist import (
    WATCHLIST
)

# -----------------------------------
# BUILD CORRELATION ENGINE
# -----------------------------------

def build_correlation_engine(

    symbols=WATCHLIST
):

    print(
        "\nLoading price history...\n"
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

        except:

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

    # -----------------------------------
    # BUILD SCORES
    # -----------------------------------

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

        # -----------------------------------
        # NORMALISE
        # Correlation range:
        #
        # -1 = excellent diversification
        # +1 = poor diversification
        # -----------------------------------

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

    return pd.DataFrame(

        rows

    ).sort_values(

        by="diversification_score",

        ascending=False
    )