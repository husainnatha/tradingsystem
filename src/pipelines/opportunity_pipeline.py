from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.market_intelligence_engine import (
    build_market_intelligence
)

from app.engine.opportunity_engine import (
    build_opportunities
)


class OpportunityPipeline:

    def run(self):

        market_context = (

            MarketPipeline()

            .run_watchlist(
                "equities"
            )
        )

        intelligence_df = (

            build_market_intelligence(
                market_context
            )
        )

        return (

            build_opportunities(
                intelligence_df
            )
        )