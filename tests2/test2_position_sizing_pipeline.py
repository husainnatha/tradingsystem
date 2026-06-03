from src.pipelines.position_sizing_pipeline import (
    PositionSizingPipeline
)

def test_position_sizing_pipeline():

    pipeline = (
        PositionSizingPipeline()
    )

    results = (
        pipeline.run()
    )

    assert (
        "position_sizing"
        in results
    )

    assert (
        "buy_recommendations"
        in results
    )