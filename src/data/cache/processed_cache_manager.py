from pathlib import Path


class ProcessedCacheManager:

    PROCESSED_DIR = Path(
        "cache/processed"
    )

    @classmethod
    def get_processed_path(
        cls,
        ticker: str,
        interval: str
    ):

        safe_ticker = ticker.replace("^", "_")

        return (
            cls.PROCESSED_DIR /
            f"{safe_ticker}_{interval}_indicators.parquet"
        )