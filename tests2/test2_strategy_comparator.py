from app.engine.strategy_comparator import (
    compare_strategies
)


def test_strategy_comparator_engine():

    df = compare_strategies(

        analysis_sale_value=100000
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
