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

from app.config.watchlist import (
    WATCHLIST
)

# -----------------------------------
# BUILD INPUTS
# -----------------------------------

position_df = (

    build_position_sizing(

        watchlist=WATCHLIST,

        portfolio_value=100000
    )
)

risk_df = (

    build_portfolio_risk()
)

rebalance_df = (

    build_rebalancing(

        portfolio_value=100000
    )
)

actions = (

    build_actions(

        rebalance_df=rebalance_df,

        position_df=position_df,

        risk_df=risk_df,

        portfolio_value=100000
    )
)

tax_df = (

    build_tax_dashboard()
)

# -----------------------------------
# DEBUG OUTPUT
# -----------------------------------

print(

    "\nREBALANCING:\n"
)

print(
    rebalance_df
)

print(

    "\nPOSITION SIZING:\n"
)

print(
    position_df
)

print(

    "\nPORTFOLIO RISK:\n"
)

print(
    risk_df
)

print(

    "\nACTIONS:\n"
)

print(
    actions
)

# -----------------------------------
# BUILD DECISIONS
# -----------------------------------

df = (

    build_decisions(

        action_df=actions,

        risk_df=risk_df,

        tax_df=tax_df
    )
)

print(

    "\nFINAL DECISIONS:\n"
)

print(

    "\nFINAL DECISIONS:\n"
)

print(

    df[
        [

            "symbol",

            "decision",

            "priority",

            "trade_value",

            "reason"
        ]
    ]
)