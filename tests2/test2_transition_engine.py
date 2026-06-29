from app.engine.transition_engine import (
    build_transition_plan
)

from app.engine.decision_engine import (
    build_decisions
)

from app.engine.action_engine import (
    build_actions
)

from app.engine.position_sizing_engine import (
    build_position_sizing
)

from app.engine.portfolio_risk_engine import (
    build_portfolio_risk
)

from app.engine.rebalancing_engine import (
    build_rebalancing
)

from app.engine.portfolio_summary import (
    get_portfolio_summary
)

from app.engine.risk_intelligence_engine import (
    build_risk_engine
)

from src.pipelines.market_pipeline import (
    MarketPipeline
)

def test_transition_engine():

    pipeline = MarketPipeline()

    market_context = (
        pipeline.run_watchlist(
            "equities"
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

    assert portfolio_value >= 0 

    symbols = list(
        market_context.get_all().keys()
    )

    assert len(symbols) > 0

    risk_intelligence_df = (

        build_risk_engine(
            verbose=False
        )
    )

    assert not risk_intelligence_df.empty

    assert "symbol", "volatility" in risk_intelligence_df.columns
    
    assert "max_drawdown", "asset_risk_score" in risk_intelligence_df.columns
           

    position_df = (

        build_position_sizing(

            market_context=market_context,

            portfolio_value=portfolio_value,

            risk_intelligence_df=risk_intelligence_df
        )
    )

    portfolio_risk_df = (

        build_portfolio_risk(
            market_context=market_context
        )
    )

    rebalance_df = (

        build_rebalancing(
            market_context=market_context,
            portfolio_value=portfolio_value
        )
    )

    actions = (

        build_actions(

            rebalance_df=rebalance_df,

            position_df=position_df,
            
            portfolio_risk_df=portfolio_risk_df,

            portfolio_value=portfolio_value
        )
    )

    decision_df = (

        build_decisions(

            action_df=actions
        )
    )

    transition_df = (

        build_transition_plan(

            decision_df=decision_df,

            position_df=position_df
        )
    )

    print(

        "\nTRANSITION PLAN:\n"
    )

    print(

        transition_df
    )
    
    assert not transition_df.empty  

    assert "symbol" in transition_df.columns