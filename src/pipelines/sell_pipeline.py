from app.engine.inventory_engine import (
    build_inventory_state
)

from app.engine.ranking_engine import (
    build_ranked_inventory
)

from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

from app.engine.capital_engine import (
    build_capital_state
)

from src.config.environment_loader import (
    EnvironmentLoader
)


class SellPipelineResult:

    def __init__(
        self,
        inventory_df,
        ranked_df,
        sale_df
    ):
        self.inventory_df = inventory_df
        self.ranked_df = ranked_df
        self.sale_df = sale_df


class SellPipeline:

    def __init__(self):

        pass
    
    capital_state = (
        build_capital_state()
    )
    
    required_sale_for_deployment = (

    capital_state[
        "required_sale_for_deployment"
    ]
)

    def run_sell_analysis(
        self,
        strategy: str = "growth"
    ):

        print(
            f"\nENVIRONMENT: "
            f"{EnvironmentLoader.get_environment().upper()}\n"
        )

        capital_state = (
            build_capital_state()
        )

        inventory_df = (
            build_inventory_state()
        )

        ranked_df = (
            build_ranked_inventory()
        )

        sale_df = optimise_sale_strategy(

            analysis_sale_value=
                capital_state[
                    "analysis_sale_value"
                ],

            strategy=strategy
        )

        print(
            "\nSell pipeline test complete.\n"
        )

        return SellPipelineResult(
            inventory_df=inventory_df,
            ranked_df=ranked_df,
            sale_df=sale_df
        )