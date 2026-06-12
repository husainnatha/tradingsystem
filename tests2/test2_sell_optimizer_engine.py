from app.engine.sell_optimizer import (
    optimise_sale_strategy
)

from app.engine.capital_engine import (
    build_capital_state
)

def test_optimse_sale_startegy():

    capital_state = build_capital_state()
    required_sale_value = 10000 #capital_state["required_sale_for_deployment"]

    df = optimise_sale_strategy(

        required_sale_value=required_sale_value,
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