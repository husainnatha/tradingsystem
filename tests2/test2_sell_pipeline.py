from src.pipelines.sell_pipeline import (
    SellPipeline
)


def test_sell_pipeline():

    pipeline = (
        SellPipeline()
    )

    results = (

        pipeline
        .run_sell_analysis()
    )

    assert "inventory_df" in results

    assert "ranked_df" in results

    assert "sell_df" in results