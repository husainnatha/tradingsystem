import pandas as pd


class MarketDataAccessor:

    @staticmethod
    def get_series(
        df: pd.DataFrame,
        column: str
    ):

        return (
            df[column]
            .squeeze()
        )

    @staticmethod
    def get_latest_value(
        df: pd.DataFrame,
        column: str
    ):

        series = (
            MarketDataAccessor
            .get_series(
                df,
                column
            )
        )

        return float(
            series.iloc[-1]
        )

    @staticmethod
    def get_latest_row(
        df: pd.DataFrame
    ):

        return df.iloc[-1]

    @staticmethod
    def get_returns(
        df: pd.DataFrame
    ):

        close = (
            MarketDataAccessor
            .get_series(
                df,
                "Close"
            )
        )

        return close.pct_change()