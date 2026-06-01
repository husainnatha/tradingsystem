from src.pipelines.market_pipeline import (
    MarketPipeline
)


pipeline = MarketPipeline()

results = pipeline.run_watchlist(
    "core_macro"
)

print(
    f"\nLoaded {len(results)} assets."
)