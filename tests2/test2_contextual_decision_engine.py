from app.engine.market_intelligence_engine import (
    build_market_intelligence
)

from app.engine.opportunity_engine import (
    build_opportunities
)

from app.engine.contextual_decision_engine import (
    build_contextual_decisions
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)


def test_contextual_decision_engine():

    market_context = (

        MarketPipeline()

        .run_watchlist(
            "equities"
        )
    )

    market_intelligence_df = (

        build_market_intelligence(
            market_context
        )
    )

    opportunity_df = (

        build_opportunities(
            market_intelligence_df
        )
    )

    decisions = (

        build_contextual_decisions(
            opportunity_df
        )
    )

    print()
    print("DECISIONS:")
    print(decisions)
    print()

    print()

    for decision in decisions:

        print()

        print(
            f"Priority: {decision['priority']}"
        )

        print(
            f"Decision: {decision['decision']}"
        )

        print(
            f"Reason: {decision['reason']}"
        )

        assert (
            decision["priority"]
            is not None
        )

        assert (
            decision["decision"]
            is not None
        )

        assert (
            decision["reason"]
            is not None
        )