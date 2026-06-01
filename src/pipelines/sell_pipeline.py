from app.engine.inventory_engine import (
    build_inventory_state
)

from app.engine.ranking_engine import (
    build_ranked_inventory
)

from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

from src.config.environment_loader import (
    EnvironmentLoader
)

class SellPipeline:

    def __init__(self):

        pass

    def run_sell_analysis(
        self,
        target_cash: float = 5000,
        strategy: str = "growth"
    ):

        print(
            f"\nENVIRONMENT: "
            f"{EnvironmentLoader.get_environment().upper()}\n"
        )

        inventory_df = (
            build_inventory_state()
        )

        ranked_df = (
            build_ranked_inventory()
        )

        sell_df = (
            optimise_sale_strategy(
                target_cash=target_cash,
                strategy=strategy
            )
        )

        print(
            "\nSell pipeline test complete.\n"
        )
        
        return {

            "inventory_df":
                inventory_df,

            "ranked_df":
                ranked_df,

            "sell_df":
                sell_df
        }