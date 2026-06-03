from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)


def test_position_sizing_engine():

    market_context = (

        MarketPipeline()

        .run_watchlist(
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
            symbols
        )
    )

    portfolio_value = (

        get_portfolio_summary()[
            "total_portfolio_value"
        ]
    )

    df = (

        build_position_sizing(
            market_context,
            portfolio_value,
            risk_intelligence_df
        )
    )

    print()

    print(df)

    assert len(df) > 0