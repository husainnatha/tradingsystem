import pandas as pd


class TechnicalIndicatorService:

    @staticmethod
    def add_moving_averages(
        df: pd.DataFrame
    ):

        df["MA50"] = (
            df["Close"]
            .rolling(window=50)
            .mean()
        )

        df["MA200"] = (
            df["Close"]
            .rolling(window=200)
            .mean()
        )

        return df

    @staticmethod
    def add_returns(
        df: pd.DataFrame
    ):

        df["Daily_Return"] = (
            df["Close"]
            .pct_change()
        )

        return df

    @staticmethod
    def add_volatility(
        df: pd.DataFrame,
        window: int = 20
    ):

        df["Volatility"] = (
            df["Daily_Return"]
            .rolling(window=window)
            .std()
        )

        return df

    @staticmethod
    def add_rsi(
        df: pd.DataFrame,
        period: int = 14
    ):

        delta = df["Close"].diff()

        gain = delta.clip(lower=0)

        loss = -delta.clip(upper=0)

        avg_gain = (
            gain.rolling(period).mean()
        )

        avg_loss = (
            loss.rolling(period).mean()
        )

        rs = avg_gain / avg_loss

        df["RSI"] = (
            100 - (100 / (1 + rs))
        )

        return df