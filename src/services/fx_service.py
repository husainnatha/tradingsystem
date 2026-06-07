import yfinance as yf


class FXService:

    @staticmethod
    def get_usd_gbp():

        ticker = yf.Ticker(
            "GBPUSD=X"
        )

        history = ticker.history(
            period="1d"
        )

        gbp_usd = float(
            history.iloc[-1]["Close"]
        )

        return (
            1 / gbp_usd
        )