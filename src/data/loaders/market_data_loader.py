import pandas as pd

from src.data.providers.yfinance_provider import YFinanceProvider
from src.data.cache.cache_manager import CacheManager

from src.data.cache.metadata_registry import (
    MetadataRegistry
)


class MarketDataLoader:

    def __init__(self):

        self.provider = YFinanceProvider()

    def load(
        self,
        ticker: str,
        period: str = "2y",
        interval: str = "1d",
        refresh: bool = False
    ):

        cache_path = CacheManager.get_cache_path(
            ticker,
            interval
        )

        if cache_path.exists() and not refresh:

            # print(f"Loading cached data: {ticker}")

            df = pd.read_parquet(cache_path)

            MetadataRegistry.save_metadata(
                ticker=ticker,
                interval=interval,
                rows=len(df)
            )

            return df

        # print(f"Downloading data: {ticker}")

        df = self.provider.download(
            ticker=ticker,
            period=period,
            interval=interval
        )

        cache_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(cache_path)

        MetadataRegistry.save_metadata(
            ticker=ticker,
            interval=interval,
            rows=len(df)
        )

        return df