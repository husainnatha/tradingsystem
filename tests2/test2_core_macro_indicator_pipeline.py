from src.pipelines.market_pipeline import (
    MarketPipeline
)

def test_core_macro_watchlist_run():

    pipeline = (
        MarketPipeline()
    )

    market_context = (
        pipeline.run_watchlist(
            "core_macro"
        )
    )

    print()

    print(
        market_context.get_all()
    )

    print()

    assert len(
        market_context.get_all()
    ) > 0
