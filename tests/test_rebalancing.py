from app.engine.rebalancing_engine import (
    build_rebalancing
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

portfolio_value = (

    get_portfolio_summary()[
        "total_portfolio_value"
    ]
)

df = (

    build_rebalancing(

        market_context=market_context,

        portfolio_value=portfolio_value
    )
)

print(df)