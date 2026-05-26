import pandas as pd
import yfinance as yf

from app.config.watchlist import (
    WATCHLIST
)


# -----------------------------------
# BUILD RISK ENGINE
# -----------------------------------

def build_risk_engine(

    symbols=WATCHLIST
):

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

            # Yahoo bulk download structure:
            # data["Close"][symbol]

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

            risk_score = min(

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

                "risk_score":
                    risk_score
            })

        except Exception as e:

            print(

                f"Failed: {symbol} : {e}"
            )

    return pd.DataFrame(

        rows
    )