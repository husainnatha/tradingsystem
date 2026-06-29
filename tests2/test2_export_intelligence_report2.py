from app.reports.export_intelligence_report import (
    export_intelligence_report
)
from src.pipelines.market_pipeline import (
    MarketPipeline
)
from app.engine.market_intelligence_engine import (
    build_market_intelligence
)

from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)
    
from app.engine.portfolio_summary import (
    get_portfolio_summary
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

from app.engine.capital_engine import (
    build_capital_state
)

from app.engine.action_engine import (
    build_actions
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.engine.rebalancing_engine import (
    build_rebalancing
)

from app.engine.transition_engine import (
    build_transition_plan
)

from app.engine.decision_engine import (
    build_decisions
)


def test_export_intelligence_report ():

    pipeline = MarketPipeline()

    market_context = (
        pipeline.run_watchlist(
            "equities"
        )
    )

    market_df = (

            build_market_intelligence(
                market_context
            )
        )
    recommendation_df = (

            build_buy_recommendations(
                market_context
            )
        )
    
    summary = (
            get_portfolio_summary()
        )

    portfolio_value = (

        summary[
            "total_portfolio_value"
        ]
    )

    risk_intelligence_df = (

            build_risk_engine(

                verbose=False
            )
        )
    
    position_df = (

        build_position_sizing(

            market_context=market_context,

            portfolio_value=portfolio_value,

            risk_intelligence_df=
                risk_intelligence_df
        )
    )

    capital_state = (
        build_capital_state()
    )

    sale_df = optimise_sale_strategy(

        analysis_sale_value=
            capital_state[
                "analysis_sale_value"
            ],

        strategy="growth"
    )
    
    portfolio_risk_df = (

            build_portfolio_risk(
                market_context
            )
        )
    
    rebalancing_df = (

            build_rebalancing(

                market_context=market_context,

                portfolio_value=portfolio_value
            )
        )

    action_df = (

            build_actions(

                rebalance_df=rebalancing_df,

                position_df=position_df,

                portfolio_risk_df=
                    portfolio_risk_df,

                portfolio_value=portfolio_value
            )
        )
    
    decision_df = (

        build_decisions(

            action_df=action_df
        )
    )

    transition_df = (

        build_transition_plan(

            decision_df=decision_df,

            position_df=position_df
        )
    )

    export_intelligence_report(

        market_df=market_df,

        recommendation_df=recommendation_df,

        position_df=position_df,

        sale_df=sale_df,

        action_df=action_df,

        transition_df=transition_df
    )

    assert True
    assert market_df is not None
    assert recommendation_df is not None
    assert position_df is not None
    assert sale_df is not None
    assert action_df is not None
    assert transition_df is not None
    assert summary is not None
    assert portfolio_value is not None
    assert risk_intelligence_df is not None
    assert capital_state is not None
    assert portfolio_risk_df is not None
    assert rebalancing_df is not None
    assert decision_df is not None
    assert transition_df is not None