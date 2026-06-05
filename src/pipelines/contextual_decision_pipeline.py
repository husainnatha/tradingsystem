from app.engine.contextual_decision_engine import (
    build_contextual_decisions
)

from app.engine.opportunity_engine import (
    build_opportunities
)

from app.engine.market_intelligence_engine import (
    build_market_intelligence
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)


class ContextualDecisionPipeline:

    def run(self):

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

        return (
            build_contextual_decisions(
                opportunity_df
            )
        )