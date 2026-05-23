import yfinance as yf
import pandas as pd

# -----------------------------------
# MACRO TICKERS
# -----------------------------------

MACRO_SYMBOLS = {

    "VIX":"^VIX",

    "US10Y":"^TNX",

    "DXY":"DX-Y.NYB",

    "SPY":"SPY",

    "QQQ":"QQQ",

    "GOLD":"GC=F",

    "BTC":"BTC-USD"
}

# -----------------------------------
# GET MACRO DATA
# -----------------------------------

def get_macro_data():

    results = {}

    for name,symbol in MACRO_SYMBOLS.items():

        try:

            ticker = yf.Ticker(
                symbol
            )

            data = ticker.history(
                period="3mo"
            )

            if data.empty:

                continue

            latest=data.iloc[-1]

            previous=data.iloc[-2]

            pct_change=round(

                (

                    latest["Close"]

                    -

                    previous["Close"]

                )

                /

                previous["Close"]

                *100,

                2
            )

            ma20 = (

                data["Close"]

                .rolling(20)

                .mean()
            )

            ma50 = (

                data["Close"]

                .rolling(50)

                .mean()
            )

            trend = False

            if (

                not pd.isna(
                    ma20.iloc[-1]
                )

                and

                not pd.isna(
                    ma50.iloc[-1]
                )
            ):

                trend = (

                    ma20.iloc[-1]

                    >

                    ma50.iloc[-1]
                )

            results[name] = {

                "price":
                    round(
                        latest["Close"],
                        2
                    ),

                "daily_change_pct":
                    pct_change,

                "trend":
                    trend
            }

        except Exception as e:

            print(

                f"Macro error: "
                f"{name}: {e}"
            )

    return results