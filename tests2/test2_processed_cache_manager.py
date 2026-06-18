import pandas as pd

from src.data.cache.processed_cache_manager import (
    ProcessedCacheManager
)

def test_processed_cache_manager():

    path = (
        ProcessedCacheManager
        .get_processed_path(
            ticker="GC=F",
            interval="1d"
        )
    )

    df = pd.read_parquet(path)

    print(df.tail())

    assert True
    