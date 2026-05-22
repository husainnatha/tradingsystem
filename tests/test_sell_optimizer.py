from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

df = optimise_sale_strategy(

    target_cash=5000
)

print("\nSELL OPTIMISER:\n")

print(df)