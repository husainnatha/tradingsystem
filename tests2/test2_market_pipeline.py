from src.pipelines.market_pipeline import (
    MarketPipeline
)

def test_market_pipeline():

    pipeline = (
        MarketPipeline()
    )

    market_context = (

        pipeline.run_watchlist(
            "equities"
        )
    )

    assert (

        market_context
        is not None
    )

    assert (

        len(
            market_context
            .get_all()
        )

        > 0
    )