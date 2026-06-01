import pandas as pd


class CorrelationService:

    @staticmethod
    def build_return_series(
        market_data: dict
    ):

        returns = pd.DataFrame()

        for ticker, df in market_data.items():

            returns[ticker] = (

                df["Close"]
                .pct_change()
            )

        return returns.dropna()

    @staticmethod
    def correlation_matrix(
        market_data: dict
    ):

        returns = (

            CorrelationService
            .build_return_series(

                market_data
            )
        )

        return returns.corr()