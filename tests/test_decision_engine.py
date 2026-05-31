from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
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

from app.engine.action_engine import (
    build_actions
)

from app.engine.decision_engine import (
    build_decisions
)

from app.reports.tax_dashboard import (
    build_tax_dashboard
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

# -----------------------------------
# BUILD MARKET CONTEXT
# -----------------------------------

pipeline = MarketPipeline()

market_context = (

    pipeline.run_watchlist(
        "equities"
    )
)

# -----------------------------------
# PORTFOLIO SUMMARY
# -----------------------------------

summary = (

    get_portfolio_summary()
)

portfolio_value = (

    summary[
        "total_portfolio_value"
    ]
)

# -----------------------------------
# RISK DATA
# -----------------------------------

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

portfolio_risk_df = (

    build_portfolio_risk(
        market_context
    )
)

# -----------------------------------
# POSITION SIZING
# -----------------------------------


# -----------------------------------
# REBALANCING
# -----------------------------------

rebalance_df = (

    build_rebalancing(

        market_context=market_context,

        portfolio_value=portfolio_value
    )
)

# -----------------------------------
# ACTIONS
# -----------------------------------

position_df = (

    build_position_sizing(

        market_context=market_context,

        portfolio_value=portfolio_value,

        risk_intelligence_df=risk_intelligence_df
    )
)

action_df = (

    build_actions(

        rebalance_df=rebalance_df,

        position_df=position_df,

        portfolio_risk_df=
            portfolio_risk_df,

        portfolio_value=
            portfolio_value
    )
)

# -----------------------------------
# TAX
# -----------------------------------

tax_df = (

    build_tax_dashboard()
)

# -----------------------------------
# DECISIONS
# -----------------------------------

decision_df = (

    build_decisions(

        action_df=action_df
    )
)

# -----------------------------------
# DEBUG OUTPUT
# -----------------------------------

print(
    "\nDECISIONS:\n"
)

print(
    decision_df.to_string()
)