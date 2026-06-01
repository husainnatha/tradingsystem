from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.action_engine import (
    build_actions
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.engine.rebalancing_engine import (
    build_rebalancing
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
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

risk_intelligence_df = (

    build_risk_engine(

        symbols=list(
            market_context
            .get_all()
            .keys()
        ),

        verbose=False
    )
)

position_df = (

    build_position_sizing(

        market_context=market_context,

        portfolio_value=portfolio_value,

        risk_intelligence_df=
            risk_intelligence_df
    )
)

portfolio_risk_df = (

    build_portfolio_risk(
        market_context
    )
)

rebalance_df = (

    build_rebalancing(

        market_context=market_context,

        portfolio_value=portfolio_value
    )
)

df = (

    build_actions(

        rebalance_df=rebalance_df,

        position_df=position_df,

        portfolio_risk_df=
            portfolio_risk_df,

        portfolio_value=
            portfolio_value
    )
)

print(
    "\nPORTFOLIO ACTIONS:\n"
)

print(
    df.to_string()
)