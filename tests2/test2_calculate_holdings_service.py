from app.engine.holdings_service import (
    calculate_holdings
)

def test_calculate_holdings():

    holdings = calculate_holdings()

    print("\nCurrent Holdings:\n")

    for symbol, data in holdings.items():

        print(
            f"{symbol} | "
            f"Qty: {data['quantity']:.2f} | "
            f"Pool Cost: £{data['pool_cost']:.2f} | "
            f"Avg Cost: £{data['avg_cost']:.2f} | "
            f"Realised PnL: £{data['realised_pnl']:.2f}"
        )

    assert len(holdings) >=1
    assert True