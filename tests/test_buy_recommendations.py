from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)


pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

df = (

    build_buy_recommendations(

        market_context
    )
)

print(

    "\nBUY RECOMMENDATIONS:\n"
)

print(
    df.to_string()
)