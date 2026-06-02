from src.pipelines.sell_pipeline import (
    SellPipeline
)

def test_sell_pipeline():

    pipeline = SellPipeline()

    pipeline.run_sell_analysis()

    assert True