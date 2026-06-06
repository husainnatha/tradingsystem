from src.pipelines.opportunity_pipeline import (
    OpportunityPipeline
)


def test_opportunity_pipeline():

    df = (

        OpportunityPipeline()

        .run()
    
        .sort_values(

            by="opportunity_score",

            ascending=False

        )
    )
    
    print(df.head(30))

    assert len(df) > 0