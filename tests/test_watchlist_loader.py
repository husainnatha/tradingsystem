from src.data.loaders.watchlist_loader import (
    WatchlistLoader
)


tickers = WatchlistLoader.load(
    "core_macro"
)

print(tickers)