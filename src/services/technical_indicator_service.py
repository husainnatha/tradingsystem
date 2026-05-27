import pandas as pd

from src.utils.dataframe_utils import (
    DataFrameUtils
)


class TechnicalIndicatorService:

    @staticmethod
    def add_moving_averages(
        df: pd.DataFrame
    ):

        close = (
            DataFrameUtils
            .get_close_series(df)
        )

        df["MA50"] = (
            close
            .rolling(window=50)
            .mean()
        )

        df["MA200"] = (
            close
            .rolling(window=200)
            .mean()
        )

        return df

    @staticmethod
    def add_returns(
        df: pd.DataFrame
    ):

        df["Daily_Return"] = (
            DataFrameUtils
            .calculate_returns(df)
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

        close = (
            DataFrameUtils
            .get_close_series(df)
        )

        delta = close.diff()

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

    @staticmethod
    def apply_all(
        df: pd.DataFrame
    ):

        print("Applying indicators...")

        df = (
            TechnicalIndicatorService
            .add_moving_averages(df)
        )

        df = (
            TechnicalIndicatorService
            .add_returns(df)
        )

        df = (
            TechnicalIndicatorService
            .add_volatility(df)
        )

        df = (
            TechnicalIndicatorService
            .add_rsi(df)
        )

        return df