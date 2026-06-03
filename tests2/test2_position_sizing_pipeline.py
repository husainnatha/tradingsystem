from src.pipelines.position_sizing_pipeline import (
    PositionSizingPipeline
)

def test_position_sizing_pipeline():

    results = (

        PositionSizingPipeline()

        .run()
    )

    print()

    print(
        results[
            "position_sizing"
        ]
    )

    print()

    print(
        results[
            "buy_recommendations"
        ]
    )

    assert True