from src.data.loaders.watchlist_loader import (
    WatchlistLoader
)

from src.services.market_data_service import (
    MarketDataService
)

from src.models.market_context import (
    MarketContext
)


class MarketPipeline:

    def __init__(self):

        self.market_service = (
            MarketDataService()
        )

    def run_watchlist(
        self,
        watchlist_name: str,
        period: str = "2y",
        interval: str = "1d"
    ):

        watchlist = (
            WatchlistLoader
            .load(watchlist_name)
        )

        context = MarketContext()

        for ticker in watchlist:

            print(
                f"\nProcessing: {ticker}"
            )

            df = (
                self.market_service
                .build_processed_dataset(
                    ticker=ticker,
                    period=period,
                    interval=interval
                )
            )

            context.add_dataset(
                ticker,
                df
            )

        return context