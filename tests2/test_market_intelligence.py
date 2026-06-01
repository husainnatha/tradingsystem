from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.market_intelligence_engine import (
    build_market_intelligence
)


pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

df = build_market_intelligence(
    market_context
)

print(df.head())