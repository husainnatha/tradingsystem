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

        f"Proceeds=£{row['estimated_proceeds']} | "

        f"Gain=£{row['estimated_gain']} | "

        f"Tax={row['tax_score']} | "

        f"Risk={row['risk_score']} | "

        f"Hold={row['holding_score']}"
    )