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

from src.pipelines.market_pipeline import (
    MarketPipeline
)


class SystemPipeline:

    def __init__(self):

        self.market_pipeline = (
            MarketPipeline()
        )

    def ensure_directories(self):

        folders = [

            "data/cache",
            "data/exports"
        ]

        for folder in folders:

            Path(folder).mkdir(

                parents=True,
                exist_ok=True
            )

    def validate_workbook(self):

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

    def rebuild_state(self):

        print(
            "Rebuilding inventory..."
        )

        build_inventory_state()

        calculate_holdings()

        build_disposal_ledger()

        build_tax_dashboard()

    def build_market_analysis(self):

        print(
            "Building market intelligence..."
        )

        market_context = (
            self.market_pipeline
            .run_watchlist(
                "core_macro"
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

        position_df = (

            build_position_sizing(

                market_context=market_context,

                portfolio_value=100000
            )
        )

        sale_df = (

            optimise_sale_strategy(

                target_cash=5000
            )
        )

        portfolio_risk_df = (

            build_portfolio_risk(
                market_context
            )
        )

        rebalancing_df = (

            build_rebalancing(

                market_context=market_context,

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

        decision_df = (

            build_decisions(

                action_df=action_df,

                risk_df=portfolio_risk_df,

                tax_df=build_tax_dashboard()
            )
        )

        transition_df = (

            build_transition_plan(

                decision_df=decision_df,

                position_df=position_df
            )
        )

        return {

            "market_df": market_df,

            "recommendation_df":
                recommendation_df,

            "position_df":
                position_df,

            "sale_df":
                sale_df,

            "action_df":
                action_df,

            "transition_df":
                transition_df
        }

    def export_reports(
        self,
        results: dict
    ):

        print(
            "Exporting workbook..."
        )

        export_intelligence_report(

            market_df=
                results["market_df"],

            recommendation_df=
                results["recommendation_df"],

            position_df=
                results["position_df"],

            sale_df=
                results["sale_df"],

            action_df=
                results["action_df"],

            transition_df=
                results["transition_df"]
        )

        generate_system_documentation()

    def run(self):

        print(
            "\nStarting System Pipeline...\n"
        )

        self.ensure_directories()

        self.validate_workbook()

        self.rebuild_state()

        results = (
            self.build_market_analysis()
        )

        self.export_reports(results)

        print(
            "\nPipeline complete.\n"
        )