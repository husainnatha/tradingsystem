from app.engine.transition_engine import (
    build_transition_plan
)

from app.engine.decision_engine import (
    build_decisions
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

from app.reports.tax_dashboard import (
    build_tax_dashboard
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

pipeline = MarketPipeline()

market_context = (
    pipeline.run_watchlist(
        "equities"
    )
)

summary = (
    get_portfolio_summary()
)

portfolio_value = (

    summary[
        "total_portfolio_value"
    ]
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

symbols = list(
    market_context.get_all().keys()
)

risk_df = (

    build_risk_engine(
        symbols=symbols,
        verbose=False
    )
)

position_df = (

    build_position_sizing(

        market_context=market_context,

        portfolio_value=portfolio_value,

        risk_df=risk_df
    )
)

rebalance_df = (

    build_rebalancing(
        market_context=market_context,
        portfolio_value=portfolio_value
    )
)

actions = (

    build_actions(

        rebalance_df=rebalance_df,

        position_df=position_df,

        risk_df=risk_df,

        portfolio_value=portfolio_value
    )
)

decision_df = (

    build_decisions(

        action_df=actions,

        risk_df=risk_df,

        tax_df=build_tax_dashboard()
    )
)

transition_df = (

    build_transition_plan(

        decision_df=decision_df,

        position_df=position_df
    )
)

print(

    "\nTRANSITION PLAN:\n"
)

print(

    transition_df
)