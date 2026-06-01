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

        self.env = (
            EnvironmentLoader.get_environment()
        )

    def run(self):

        print(
            f"\nENVIRONMENT: "
            f"{self.env.upper()}\n"
        )

        sell_df = (

            optimise_sale_strategy(

                target_cash=5000,

                strategy="growth"
            )
        )

        inventory_df = (
            build_inventory_state()
        )

        ranked_df = (
            build_ranked_inventory()
        )

        return {

            "inventory_df":
                inventory_df,

            "ranked_df":
                ranked_df,

            "sell_df":
                sell_df
        }