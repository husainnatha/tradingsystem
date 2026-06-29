import pandas as pd

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

    pd.set_option(
        "display.max_columns",
        None
    )

    pd.set_option(
        "display.width",
        None
    )

    print()

    print(
        df.head(20)
    )

    # print(
    #     df[
    #         [
    #             "symbol",
    #             "suggested_allocation_pct",
    #             "theoretical_position_value",
    #             "executable_position_value",
    #             "capital_status",
    #             "asset_risk_score",
    #             "portfolio_risk"
    #         ]
    #     ]
    #     .head(20)
    # )
    # print()

    assert len(df) > 0