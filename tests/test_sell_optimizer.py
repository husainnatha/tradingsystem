from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

df = optimise_sale_strategy(

    target_cash=5000,
    strategy="growth"
)

print("\nSELL OPTIMISER:\n")

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"AI={row['ai_score']} | "

        f"SellQty={row['sell_quantity']} | "

        f"Gain=£{row['estimated_gain']} \n"

        f"Explanation: "

        f"{row['explanation']}\n"
    )