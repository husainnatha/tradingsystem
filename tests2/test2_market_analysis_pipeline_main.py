from src.pipelines.system_pipeline import (
    SystemPipeline
)

def test_market_analysis():

    pipeline = SystemPipeline()

    results = (
        pipeline.build_market_analysis()
    )

    assert "market_df" in results
    assert "position_df" in results