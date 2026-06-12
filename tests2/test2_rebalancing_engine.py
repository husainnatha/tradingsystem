from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.rebalancing_engine import (
    build_rebalancing
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)

def test_rebalancing_engine():

    pipeline = (
            MarketPipeline()
        )

    market_context = (

    pipeline.run_watchlist(
                "equities"
            )
        )

    portfolio = get_portfolio_summary()

    portfolio_value = portfolio["total_portfolio_value"]

    df = (

        build_rebalancing(

            market_context=market_context,

            portfolio_value=portfolio_value
        )
    )

    print(df)
    assert True
    assert df is not None
    assert portfolio_value >= 0