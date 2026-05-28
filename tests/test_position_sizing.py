from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)


pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "core_macro"
    )
)

df = build_position_sizing(

    market_context=market_context,

    portfolio_value=100000
)

print(df.head())