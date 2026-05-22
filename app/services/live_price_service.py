import yfinance as yf

# -----------------------------------
# GET LIVE PRICE
# -----------------------------------

def get_live_price(

    symbol
):

    try:

        ticker = yf.Ticker(symbol)

        data = ticker.history(
            period="1d"
        )

        if data.empty:

            return None

        latest_price = data[
            "Close"
        ].iloc[-1]

        return round(
            float(latest_price),
            2
        )

    except Exception as e:

        print(

            f"Price lookup failed "
            f"for {symbol}: {e}"
        )

        return None