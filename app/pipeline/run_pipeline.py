from pathlib import Path

from scripts.import_transactions import (
    import_transactions
)

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

# -----------------------------------
# RUN FULL PIPELINE
# -----------------------------------

def run_pipeline():

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
    # IMPORT TRANSACTIONS
    # -----------------------------------

    print(
        "Importing transactions..."
    )

    import_transactions()

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

    build_market_intelligence(
        WATCHLIST
    )

    build_buy_recommendations(
        WATCHLIST
    )

    build_position_sizing(

        watchlist=WATCHLIST,

        portfolio_value=100000
    )

    optimise_sale_strategy(

        target_cash=5000
    )

    # -----------------------------------
    # EXPORT
    # -----------------------------------

    print(
        "Exporting workbook..."
    )

    export_intelligence_report()

    print(
        "\nPipeline complete.\n"
    )


if __name__ == "__main__":

    run_pipeline()