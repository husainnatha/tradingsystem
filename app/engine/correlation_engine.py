import pandas as pd

from app.services.market_data_service import (
    load_market_prices
)

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

    print(
    "\nRequesting market prices...\n"
)

    # -----------------------------------
    # LOAD CACHED / DOWNLOADED DATA
    # -----------------------------------

    market_data = (

        load_market_prices(

            symbols
        )
    )

    prices = pd.DataFrame()

    # -----------------------------------
    # EXTRACT CLOSE PRICES
    # -----------------------------------

    for symbol in symbols:

        try:

            prices[symbol] = (

                market_data[
                    symbol
                ][
                    "Close"
                ]
            )

        except Exception as e:

            print(

                f"Failed: {symbol}: {e}"
            )

    # -----------------------------------
    # DAILY RETURNS
    # -----------------------------------

    returns = (

        prices

        .pct_change()

        .dropna()
    )

    correlation = (

        returns.corr()
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

    return pd.DataFrame(

        rows

    ).sort_values(

        by="diversification_score",

        ascending=False
    )