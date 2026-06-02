from src.pipelines.sell_pipeline import (
    SellPipeline
)

def test_sell_pipeline():

    pipeline = SellPipeline()

    results = pipeline.run_sell_analysis()

    assert results.inventory_df is not None

    assert results.ranked_df is not None

    assert results.sell_df is not None

    print(results.inventory_df.head())
    print(results.ranked_df.head())
    print(results.sell_df.head())

   