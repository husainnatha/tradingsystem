from app.engine.strategy_comparator import (
    compare_strategies
)

df = compare_strategies(

    target_cash=5000
)

print("\nSTRATEGY COMPARISON:\n")

for _, row in df.iterrows():

    print(

        f"{row['strategy']} | "

        f"{row['symbol']} | "

        f"SellQty={row['sell_quantity']} | "

        f"Gain=£{row['estimated_gain']} | "

        f"AI={row['ai_score']}"
    )