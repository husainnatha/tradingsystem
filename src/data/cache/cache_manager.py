from pathlib import Path


class CacheManager:

    RAW_CACHE_DIR = Path("cache/raw")

    @classmethod
    def get_cache_path(
        cls,
        ticker: str,
        interval: str
    ):

        safe_ticker = ticker.replace("^", "_")

        return cls.RAW_CACHE_DIR / f"{safe_ticker}_{interval}.parquet"