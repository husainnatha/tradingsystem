import pandas as pd

from src.data.cache.processed_cache_manager import (
    ProcessedCacheManager
)


path = (
    ProcessedCacheManager
    .get_processed_path(
        ticker="GC=F",
        interval="1d"
    )
)

df = pd.read_parquet(path)

print(df.tail())