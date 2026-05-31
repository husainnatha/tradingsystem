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

from app.engine.market_context_engine import (
    build_market_context
)

market_context = (

    build_market_context()
)

position_df = (

    build_position_sizing(

        market_context=market_context,

        portfolio_value=100000
    )
)

risk_intelligence_df = (

    build_portfolio_risk(

        market_context
    )
)

rebalance_df = (

    build_rebalancing(

        market_context=market_context,

        portfolio_value=100000
    )
)

df = (

    build_actions(

        rebalance_df=rebalance_df,

        position_df=position_df,

        risk_intelligence_df=risk_intelligence_df,

        portfolio_value=100000
    )
)

print(

    "\nPORTFOLIO ACTIONS:\n"
)

print(df)