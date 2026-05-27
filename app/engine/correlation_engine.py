import pandas as pd

# -----------------------------------
# CACHE
# -----------------------------------

_cached_correlation_df = None

# -----------------------------------
# BUILD CORRELATION ENGINE
# -----------------------------------

def build_correlation_engine(
    market_context
):

    
    # -----------------------------------
    # EXTRACT CLOSE PRICES
    # -----------------------------------

    prices = pd.DataFrame()

    for symbol, df in (
        market_context
        .get_all()
        .items()
    ):

        try:

            prices[symbol] = (

                df["Close"]
                .squeeze()
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