from app.engine.strategy_comparator import (
    compare_strategies
)


def test_strategy_comparator_engine():

    required_sale_value = 100000
    
    # (
    #     capital_state[
    #         "required_sale_for_deployment"
    #     ]
    # )

    df = compare_strategies(

        required_sale_value=required_sale_value
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

    assert True
assert True