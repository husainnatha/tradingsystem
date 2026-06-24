from src.data.loaders.watchlist_loader import (
    WatchlistLoader
)

def test_watchlist_loader():

    tickers = WatchlistLoader.load(
        "equities"
    )

    assert len(tickers) > 1

