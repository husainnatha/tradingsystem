import yfinance as yf


class YFinanceProvider:

    def download(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d"
    ):

        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )

        return df