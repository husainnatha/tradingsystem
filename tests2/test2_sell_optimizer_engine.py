from app.engine.sell_optimizer import (
    optimise_sale_strategy
)


def test_optimse_sale_startegy():


    df = optimise_sale_strategy(

        analysis_sale_value=25000,
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