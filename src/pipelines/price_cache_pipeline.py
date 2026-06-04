from src.pipelines.market_pipeline import (
    MarketPipeline
)

from src.services.price_cache_service import (
    PriceCacheService
)


class PriceCachePipeline:

    def run(self):

        market_context = (

            MarketPipeline()

            .run_watchlist(
                "equities"
            )
        )

        symbols = list(

            market_context
            .get_all()
            .keys()
        )

        print(
            "\nRefreshing prices...\n"
        )

        for symbol in symbols:

            PriceCacheService.refresh_price(
                symbol
            )

        print(
            f"\nCached "
            f"{len(symbols)} symbols.\n"
        )