from pathlib import Path
from datetime import (
    datetime,
    timedelta
)

import pandas as pd


class ProcessedCacheManager:

    PROCESSED_DIR = Path(
        "cache/processed"
    )

    CACHE_EXPIRY_DAYS = 1

    @classmethod
    def get_processed_path(
        cls,
        ticker: str,
        interval: str
    ):

        safe_ticker = ticker.replace(
            "^",
            "_"
        )

        return (
            cls.PROCESSED_DIR
            /
            f"{safe_ticker}_{interval}_indicators.parquet"
        )

    @classmethod
    def exists(
        cls,
        ticker: str,
        interval: str
    ):

        return cls.get_processed_path(
            ticker,
            interval
        ).exists()

    @classmethod
    def load(
        cls,
        ticker: str,
        interval: str
    ):

        path = cls.get_processed_path(
            ticker,
            interval
        )

        if not path.exists():

            return None

        return pd.read_parquet(
            path
        )

    @classmethod
    def save(
        cls,
        ticker: str,
        interval: str,
        df
    ):

        path = cls.get_processed_path(
            ticker,
            interval
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(
            path
        )

    @classmethod
    def is_cache_fresh(
        cls,
        ticker: str,
        interval: str
    ):

        path = cls.get_processed_path(
            ticker,
            interval
        )

        if not path.exists():

            return False

        modified = datetime.fromtimestamp(
            path.stat().st_mtime
        )

        age = (
            datetime.now()
            - modified
        )

        return age < timedelta(
            days=cls.CACHE_EXPIRY_DAYS
        )