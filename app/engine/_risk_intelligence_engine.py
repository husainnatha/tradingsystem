import pandas as pd
import yfinance as yf


# -----------------------------------
# BUILD RISK ENGINE
# -----------------------------------

def build_risk_engine(

    symbols,

    verbose=True
):

    if verbose:

        print(

            "\nBuilding risk intelligence...\n"
        )

    rows = []

    symbols_string = " ".join(

        symbols
    )

    data = yf.download(

        symbols_string,

        period="6mo",

        group_by="ticker",

        progress=False
    )

    for symbol in symbols:

        try:

            prices = (

                data[
                    symbol
                ][
                    "Close"
                ]
            )

            returns = (

                prices
                .pct_change()
                .dropna()
            )

            volatility = (

                returns.std()

                * (252 ** 0.5)
            )

            rolling_max = (

                prices.cummax()
            )

            drawdown = (

                (prices - rolling_max)

                / rolling_max
            )

            max_drawdown = (

                drawdown.min()
            )

            raw_score = (

                volatility

                + abs(
                    max_drawdown
                )
            )

            asset_risk_score = min(

                round(

                    raw_score / 2,

                    4
                ),

                1.0
            )

            rows.append({

                "symbol":
                    symbol,

                "volatility":
                    round(
                        volatility,
                        4
                    ),

                "max_drawdown":
                    round(
                        max_drawdown,
                        4
                    ),

                "asset_risk_score":
                    asset_risk_score
            })

        except Exception as e:

            print(

                f"Failed: {symbol}: {e}"
            )

    return pd.DataFrame(

        rows
    )