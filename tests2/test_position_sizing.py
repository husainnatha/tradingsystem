from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from src.services.capital_service import (
    CapitalService
)

config = (
    CapitalService()
    .get_capital_config()   
)

portfolio_value = 100000

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

from app.engine.risk_engine import (
    build_risk_engine
)

symbols = list(

    market_context
    .get_all()
    .keys()
)

risk_df = (

    build_risk_engine(

        symbols=symbols,

        verbose=True
    )
)

df = (

    build_position_sizing(

        market_context=market_context,

        portfolio_value=portfolio_value,

        risk_df=risk_df
    )
)

print(df.head())