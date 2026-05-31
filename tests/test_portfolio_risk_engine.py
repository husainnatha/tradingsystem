from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

df = (

    build_portfolio_risk(
        market_context=market_context
    )
)

print(

    "\nPORTFOLIO RISK:\n"
)

print(

    df.to_string()
)