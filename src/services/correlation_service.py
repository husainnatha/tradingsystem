import pandas as pd


class CorrelationService:

    @staticmethod
    def build_return_series(
        market_context
    ):

        returns = pd.DataFrame()

        for ticker, df in (
            market_context
                .get_all()
                .items()
        ):
            returns[ticker] = (

                df["Close"]
                .pct_change()
            )

        return returns.dropna()

    @staticmethod
    def correlation_matrix(
        market_context
    ):

        returns = (

            CorrelationService
            .build_return_series(

                market_context
            )
        )

        return returns.corr()