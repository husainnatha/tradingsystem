from app.engine.risk_intelligence_engine import (

    build_risk_engine
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

symbols = list(

    market_context
    .get_all()
    .keys()
)

risk_intelligence_df = (

    build_risk_engine(

        symbols=symbols,

        verbose=True
    )
)
risk_intelligence_df = (

    risk_intelligence_df.sort_values(

        by="asset_risk_score",

        ascending=False
    )
)

print(

    "\nRISK INTELLIGENCE:\n"
)

print(

    risk_intelligence_df.to_string()
)