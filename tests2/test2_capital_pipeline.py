from src.pipelines.capital_pipeline import (
    CapitalPipeline
)


def test_capital_pipeline():

    pipeline = (
        CapitalPipeline()
    )

    results = (
        pipeline.run()
    )

    assert (
        "capital_state"
        in results
    )

    assert (
        "capital_summary"
        in results
    )