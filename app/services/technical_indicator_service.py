import yfinance as yf

import pandas as pd

# -----------------------------------
# GET TECHNICAL INDICATORS
# -----------------------------------

def get_technical_indicators(

    symbol
):

    try:

        df = yf.Ticker(

            symbol

        ).history(

            period="1y"
        )

        if df.empty:

            return None

        # -----------------------------------
        # MOVING AVERAGES
        # -----------------------------------

        df[
            "MA50"
        ] = df[
            "Close"
        ].rolling(
            50
        ).mean()

        df[
            "MA200"
        ] = df[
            "Close"
        ].rolling(
            200
        ).mean()

        # -----------------------------------
        # RSI
        # -----------------------------------

        delta = df[
            "Close"
        ].diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

        avg_gain = gain.rolling(
            14
        ).mean()

        avg_loss = loss.rolling(
            14
        ).mean()

        rs = avg_gain / avg_loss

        df[
            "RSI"
        ] = 100 - (

            100 / (1 + rs)
        )

        latest = df.iloc[-1]

        return {

            "symbol":
                symbol,

            "price":
                round(
                    latest["Close"],
                    2
                ),

            "ma50":
                round(
                    latest["MA50"],
                    2
                ),

            "ma200":
                round(
                    latest["MA200"],
                    2
                ),

            "rsi":
                round(
                    latest["RSI"],
                    2
                ),

            "bullish_trend":

                latest["MA50"]

                >

                latest["MA200"]
        }

    except Exception as e:

        print(

            f"Indicator lookup failed "
            f"for {symbol}: {e}"
        )

        return None