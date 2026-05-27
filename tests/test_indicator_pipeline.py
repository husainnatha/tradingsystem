from src.data.loaders.market_data_loader import (
    MarketDataLoader
)

from src.services.technical_indicator_service import (
    TechnicalIndicatorService
)

from src.data.cache.processed_cache_manager import (
    ProcessedCacheManager
)

loader = MarketDataLoader()

df = loader.load(
    ticker="GC=F",
    period="2y"
)


df = (
    TechnicalIndicatorService
    .add_moving_averages(df)
)

df = (
    TechnicalIndicatorService
    .add_returns(df)
)

df = (
    TechnicalIndicatorService
    .add_volatility(df)
)

df = (
    TechnicalIndicatorService
    .add_rsi(df)
)

processed_path = (
    ProcessedCacheManager
    .get_processed_path(
        ticker="GC=F",
        interval="1d"
    )
)

processed_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_parquet(processed_path)

print(
    f"\nSaved processed indicators:"
    f"\n{processed_path}"
)

print(
    df[
        [
            "Close",
            "MA50",
            "MA200",
            "Daily_Return",
            "Volatility",
            "RSI"
        ]
    ].tail()
)