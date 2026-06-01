from app.engine.market_context_engine import (
    build_market_context
)

from app.engine.rebalancing_engine import (
    build_rebalancing
)

market_context = (
    build_market_context()
)

df = (

    build_rebalancing(

        market_context=market_context,

        portfolio_value=100000
    )
)

print(df)