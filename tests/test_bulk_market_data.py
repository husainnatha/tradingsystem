from src.data.loaders.watchlist_loader import (
    WatchlistLoader
)

from src.data.loaders.market_data_loader import (
    MarketDataLoader
)


watchlist = WatchlistLoader.load(
    "core_macro"
)

loader = MarketDataLoader()

market_data = {}


for ticker in watchlist:

    print(f"\nProcessing: {ticker}")

    df = loader.load(
        ticker=ticker,
        period="2y",
        interval="1d"
    )

    market_data[ticker] = df

    print(df.tail(2))


print("\nCompleted market data load.")