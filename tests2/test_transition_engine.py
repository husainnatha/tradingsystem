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

from app.config.watchlist import (
    WATCHLIST
)

position_df = (

    build_position_sizing(

        watchlist=WATCHLIST,

        portfolio_value=100000
    )
)

risk_intelligence_df = (

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

        risk_intelligence_df=risk_intelligence_df,

        portfolio_value=100000
    )
)

decision_df = (

    build_decisions(

        action_df=actions,

        risk_intelligence_df=risk_intelligence_df,

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