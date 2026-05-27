from src.data.loaders.market_data_loader import (
    MarketDataLoader
)

from src.services.technical_indicator_service import (
    TechnicalIndicatorService
)

from src.data.cache.processed_cache_manager import (
    ProcessedCacheManager
)


class MarketDataService:

    def __init__(self):

        self.loader = MarketDataLoader()

    def build_processed_dataset(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d"
    ):

        df = self.loader.load(
            ticker=ticker,
            period=period,
            interval=interval
        )

        df = (
            TechnicalIndicatorService
            .apply_all(df)
        )

        processed_path = (
            ProcessedCacheManager
            .get_processed_path(
                ticker,
                interval
            )
        )

        processed_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(processed_path)

        return df