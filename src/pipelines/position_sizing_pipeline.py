from src.pipelines.market_pipeline import (
    MarketPipeline
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)

class PositionSizingPipeline:

    def run(self):

        market_context = (

            MarketPipeline()

            .run_watchlist(
                "equities"
            )
        )

        symbols = list(

            market_context
            .get_all()
            .keys()
        )

        portfolio_value = (

            get_portfolio_summary()[

                "total_portfolio_value"
            ]
        )

        risk_intelligence_df = (

            build_risk_engine(

                symbols=symbols,

                verbose=False
            )
        )

        return {

            "position_sizing":

                build_position_sizing(

                    market_context,

                    portfolio_value,

                    risk_intelligence_df
                ),

            "buy_recommendations":

                build_buy_recommendations(
                    market_context
                )
        }