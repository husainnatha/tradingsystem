from src.pipelines.market_pipeline import (
    MarketPipeline
)

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

print(type(market_context))

print(type(
    market_context.get_all()
))