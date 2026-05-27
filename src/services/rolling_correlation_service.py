import pandas as pd


class RollingCorrelationService:

    @staticmethod
    def rolling_correlation(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        window: int = 60
    ):

        returns_1 = (
            df1["Close"]
            .squeeze()
            .pct_change()
        )

        returns_2 = (
            df2["Close"]
            .squeeze()
            .pct_change()
        )

        rolling_corr = (
            returns_1
            .rolling(window)
            .corr(returns_2)
        )

        result = pd.DataFrame({

            "Rolling_Correlation":
                rolling_corr

        })

        return result.dropna()