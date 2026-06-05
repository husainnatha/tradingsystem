from src.pipelines.contextual_decision_pipeline import (
    ContextualDecisionPipeline
)

def test_contextual_decision_pipeline():

    decisions = (

        ContextualDecisionPipeline()

        .run()
    )

    for decision in decisions:

        print()
        print(
            decision
        )

    assert len(
        decisions
    ) > 0