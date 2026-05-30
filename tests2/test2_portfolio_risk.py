from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)


def test_portfolio_risk():

    pipeline = MarketPipeline()

    market_context = (
        pipeline.run_watchlist(
            "equities"
        )
    )

    df = (
        build_portfolio_risk(
            market_context=market_context
        )
    )

    assert not df.empty

    assert "symbol" in df.columns

    assert "portfolio_risk" in df.columns