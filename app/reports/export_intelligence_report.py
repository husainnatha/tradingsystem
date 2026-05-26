import pandas as pd
from pathlib import Path

from app.database.db import (
    SessionLocal
)

from app.database.models import (
    Transaction
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

from app.engine.inventory_engine import (
    build_inventory_state
)

from app.engine.sell_optimizer import (
    optimise_sale_strategy
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

from app.engine.sector_intelligence import (
    build_sector_exposure
)

from app.engine.strategy_comparator import (
    compare_strategies
)

from app.config.watchlist import (
    WATCHLIST
)

from app.config.environment import (

    get_output_suffix
)

from app.config.environment import (

    EXPORT_DIR,

    get_output_suffix
)
# -----------------------------------
# EXPORT INTELLIGENCE REPORT
# -----------------------------------

def export_intelligence_report():

    env = get_output_suffix()

    output_file = (

        EXPORT_DIR

        / f"{env}-portfolio_intelligence.xlsx"
    )

    # -----------------------------------
    # BUILD DATAFRAMES
    # -----------------------------------

        # -----------------------------------
    # HOLDINGS DATAFRAME
    # -----------------------------------

    holdings_data = calculate_holdings()

    holdings_rows = []

    for symbol, data in holdings_data.items():

        holdings_rows.append({

            "symbol":
                symbol,

            "quantity":
                round(
                    data["quantity"],
                    2
                ),

            "pool_cost":
                round(
                    data["pool_cost"],
                    2
                ),

            "avg_cost":
                round(
                    data["avg_cost"],
                    2
                ),

            "realised_pnl":
                round(
                    data["realised_pnl"],
                    2
                )
        })

    holdings_df = pd.DataFrame(
        holdings_rows
    )

    disposal_df = build_disposal_ledger()

    tax_df = build_tax_dashboard()

    inventory_df = build_inventory_state()

    sell_df = optimise_sale_strategy(

        target_cash=5000
    )

    market_df = build_market_intelligence(
        WATCHLIST
    )

    buy_df = build_buy_recommendations(
        WATCHLIST
    )

    sizing_df = build_position_sizing(

        watchlist=WATCHLIST,

        portfolio_value=100000
    )

    sector_df = build_sector_exposure()

    strategy_df = compare_strategies(
        target_cash=5000
    )

    # -----------------------------------
    # TRANSACTIONS
    # -----------------------------------

    session = SessionLocal()

    transactions = session.query(
        Transaction
    ).all()

    transaction_rows = []

    for tx in transactions:

        transaction_rows.append({

            "trade_date":
                tx.trade_date,

            "account":
                tx.account,

            "symbol":
                tx.symbol,

            "action":
                tx.action,

            "quantity":
                tx.quantity,

            "trade_price":
                tx.trade_price,

            "fees":
                tx.fees,

            "fx_rate_to_gbp":
                tx.fx_rate_to_gbp
        })

    transactions_df = pd.DataFrame(
        transaction_rows
    )

    session.close()

        # -----------------------------------
    # ENSURE EXPORT DIRECTORY EXISTS
    # -----------------------------------

    export_dir = Path(
        "data/exports"
    )

    export_dir.mkdir(

        parents=True,

        exist_ok=True
    )

    # -----------------------------------
    # EXPORT EXCEL
    # -----------------------------------

    with pd.ExcelWriter(

        output_file,

        engine="openpyxl"
    ) as writer:

        transactions_df.to_excel(

            writer,

            sheet_name="TRANSACTIONS",

            index=False
        )

        holdings_df.to_excel(

            writer,

            sheet_name="HOLDINGS",

            index=False
        )

        disposal_df.to_excel(

            writer,

            sheet_name="DISPOSAL_LEDGER",

            index=False
        )

        tax_df.to_excel(

            writer,

            sheet_name="TAX_DASHBOARD",

            index=False
        )

        inventory_df.to_excel(

            writer,

            sheet_name="INVENTORY",

            index=False
        )

        sell_df.to_excel(

            writer,

            sheet_name="SELL_OPTIMISER",

            index=False
        )

        market_df.to_excel(

            writer,

            sheet_name="MARKET_INTELLIGENCE",

            index=False
        )

        buy_df.to_excel(

            writer,

            sheet_name="BUY_RECOMMENDATIONS",

            index=False
        )

        sizing_df.to_excel(

            writer,

            sheet_name="POSITION_SIZING",

            index=False
        )

        sector_df.to_excel(

            writer,

            sheet_name="SECTOR_EXPOSURE",

            index=False
        )

        strategy_df.to_excel(

            writer,

            sheet_name="STRATEGY_COMPARISON",

            index=False
        )

    print(

        f"\nPortfolio intelligence report "
        f"exported:\n{output_file}\n"
    )