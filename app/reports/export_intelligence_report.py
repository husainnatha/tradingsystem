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

from app.engine.sector_intelligence import (
    build_sector_exposure
)

from app.engine.strategy_comparator import (
    compare_strategies
)

from app.config.environment import (

    EXPORT_DIR,

    get_output_suffix
)

from app.engine.capital_engine import (
    build_capital_summary
)

from app.engine.capital_engine import (
    build_capital_state
)

from app.engine.macro_regime_engine import (
    build_macro_regime
)

from app.engine.opportunity_engine import (
    build_opportunities
)

from app.engine.contextual_decision_engine import (
    build_contextual_decisions
)


# -----------------------------------
# EXPORT INTELLIGENCE REPORT
# -----------------------------------

def export_intelligence_report(
    market_df,
    recommendation_df,
    position_df,
    sale_df,
    action_df,
    transition_df,
    capital_df=None,
    macro_df=None,
    opportunity_df=None,
    contextual_decisions_df=None
):
    env = get_output_suffix()

    output_file = (

        EXPORT_DIR

        / f"{env}-portfolio_intelligence.xlsx"
    )

    # -----------------------------------
    # HOLDINGS
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

    # -----------------------------------
    # OTHER DATA
    # -----------------------------------

    disposal_df = (

        build_disposal_ledger()
    )

    tax_df = (

        build_tax_dashboard()
    )

    inventory_df = (

        build_inventory_state()
    )

    sector_df = (

        build_sector_exposure()
    )

    capital_state = (
        build_capital_state()
    )

    if capital_df is None:
        capital_df = build_capital_summary()

    if macro_df is None:
        macro_df = pd.DataFrame([
            build_macro_regime()
        ])

    if opportunity_df is None:
        opportunity_df = build_opportunities(
            market_df
        )

    if contextual_decisions_df is None:
        contextual_decisions_df = pd.DataFrame(
            build_contextual_decisions(
                opportunity_df
            )
        )

    target_cash = (
        capital_state[
            "required_sale_for_deployment"
        ]
    )

    strategy_df = (

        compare_strategies(
            target_cash=target_cash
        )
    )

    print(
        f"Required Sale Value: "
        f"£{capital_state['required_sale_for_deployment']:,.2f}"
    )

    buy_df = (

        recommendation_df
    )

    sizing_df = (

        position_df
    )

    sell_df = (

        sale_df
    )

    actions_df = (

        action_df
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
    # ENSURE DIRECTORY
    # -----------------------------------

    Path(

        EXPORT_DIR

    ).mkdir(

        parents=True,

        exist_ok=True
    )

    # -----------------------------------
    # EXPORT
    # -----------------------------------

    with pd.ExcelWriter(

        output_file,

        engine="xlsxwriter"

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

        sell_df.to_excel(

            writer,

            sheet_name="SELL_OPTIMISER",

            index=False
        )

        actions_df.to_excel(

            writer,

            sheet_name="ACTIONS",

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

        transition_df.to_excel(

            writer,

            sheet_name="TRANSITIONS",

            index=False
        ),
    
        macro_df.to_excel(

            writer,

            sheet_name="MACRO_REGIME",

            index=False
        ),
    
        opportunity_df.to_excel(

            writer,

            sheet_name="OPPORTUNITY_LEDGER",

            index=False
        ),
    
        contextual_decisions_df.to_excel(

            writer,

            sheet_name="CONTEXTUAL_DECISIONS",

            index=False
        ),
    
        capital_df.to_excel(

            writer,

            sheet_name="CAPITAL_SUMMARY",

            index=False
        )

    print(

        f"\nPortfolio intelligence report "
        f"exported:\n{output_file}\n"
    )