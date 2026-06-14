import yfinance as yf


class FXService:

    FALLBACK_USD_GBP = 0.79

    @staticmethod
    def get_usd_gbp():

        try:

            ticker = yf.Ticker(
                "GBPUSD=X"
            )

            history = ticker.history(
                period="5d"
            )

            if history.empty:

                raise ValueError(
                    "No FX data returned"
                )

            gbp_usd = float(
                history.iloc[-1]["Close"]
            )

            return (
                1 / gbp_usd
            )

        except Exception as ex:

            print(
                f"WARNING: FX lookup failed: {ex}"
            )

            return (
                FXService
                .FALLBACK_USD_GBP
            )