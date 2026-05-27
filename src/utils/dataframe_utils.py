import pandas as pd


class DataFrameUtils:

    @staticmethod
    def get_close_series(
        df: pd.DataFrame
    ):

        return (
            df["Close"]
            .squeeze()
        )

    @staticmethod
    def calculate_returns(
        df: pd.DataFrame
    ):

        return (
            DataFrameUtils
            .get_close_series(df)
            .pct_change()
        )