from pathlib import Path

from app.engine.inventory_engine import (
    build_inventory_state
)

from app.engine.holdings_service import (
    calculate_holdings
)

from app.engine.disposal_ledger import (
    build_disposal_ledger
)

from app.reports.tax_dashboard import (
    build_tax_dashboard
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

from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

from app.reports.export_intelligence_report import (
    export_intelligence_report
)

from app.config.watchlist import (
    WATCHLIST
)

from app.reports.documentation_generator import (
    generate_system_documentation
)

from app.database.models import (
    Base
)

from app.database.db import (
    engine
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

# -----------------------------------
# RUN FULL PIPELINE
# -----------------------------------

def run_pipeline():

    print(

    "\nInitializing database...\n"
    )

    Base.metadata.create_all(

        bind=engine
    )

    print(
        "\nStarting Trading System Pipeline...\n"
    )

    # -----------------------------------
    # ENSURE FOLDERS EXIST
    # -----------------------------------

    folders = [

        "data/cache",
        "data/exports"
    ]

    for folder in folders:

        Path(
            folder
        ).mkdir(

            parents=True,

            exist_ok=True
        )

    workbook = (

        Path.cwd()

        / "dashboard"

        / "trading_system.xlsx"
    )

    if not workbook.exists():

        raise FileNotFoundError(

            f"\nWorkbook not found:\n"
            f"{workbook}\n"
        )

    # -----------------------------------
    # REBUILD STATE
    # -----------------------------------

    print(
        "Rebuilding inventory..."
    )

    build_inventory_state()

    calculate_holdings()

    build_disposal_ledger()

    build_tax_dashboard()

    # -----------------------------------
    # MARKET INTELLIGENCE
    # -----------------------------------

    print(
        "Building market intelligence..."
    )

    market_df = (

        build_market_intelligence(
            WATCHLIST
        )
    )

    recommendation_df = (

        build_buy_recommendations(
            WATCHLIST
        )
    )

    position_df = (

        build_position_sizing(

            watchlist=WATCHLIST,

            portfolio_value=100000
        )
    )

    sale_df = (

        optimise_sale_strategy(

            target_cash=5000
        )
    )

    portfolio_risk_df = (

        build_portfolio_risk()
    )

    rebalancing_df = (

        build_rebalancing(
            portfolio_value=100000
        )
    )

    action_df = (

        build_actions(

            rebalance_df=rebalancing_df,

            position_df=position_df,

            risk_df=portfolio_risk_df,

            portfolio_value=100000
        )
    )

    # -----------------------------------
    # DECISIONS
    # -----------------------------------

    decision_df = (

        build_decisions(

            action_df=action_df,

            risk_df=portfolio_risk_df,

            tax_df=build_tax_dashboard()
        )
    )

    # -----------------------------------
    # TRANSITION PLAN
    # -----------------------------------

    transition_df = (

        build_transition_plan(

            decision_df=decision_df,

            position_df=position_df
        )
    )

    # -----------------------------------
    # EXPORT
    # -----------------------------------

    print(
        "Exporting workbook..."
    )

    export_intelligence_report(

        market_df=market_df,

        recommendation_df=recommendation_df,

        position_df=position_df,

        sale_df=sale_df,

        action_df=action_df,

        transition_df=transition_df
    )

    generate_system_documentation()

    print(
        "\nPipeline complete.\n"
    )

    

if __name__ == "__main__":

    run_pipeline()