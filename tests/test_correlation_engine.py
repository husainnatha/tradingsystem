from src.data.loaders.watchlist_loader import (
    WatchlistLoader
)

from src.data.loaders.market_data_loader import (
    MarketDataLoader
)

from src.services.correlation_service import (
    CorrelationService
)


watchlist = WatchlistLoader.load(
    "core_macro"
)

loader = MarketDataLoader()

market_data = {}


for ticker in watchlist:

    print(f"Loading: {ticker}")

    df = loader.load(
        ticker=ticker,
        period="2y"
    )

    market_data[ticker] = df


correlation_matrix = (
    CorrelationService
    .correlation_matrix(
        market_data
    )
)


print("\nCorrelation Matrix:\n")

print(
    correlation_matrix.round(2)
)