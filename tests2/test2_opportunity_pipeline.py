from src.pipelines.opportunity_pipeline import (
    OpportunityPipeline
)


def test_opportunity_pipeline():

    df = (

        OpportunityPipeline()

        .run()
    )

    print(df.head(10))

    assert len(df) > 0