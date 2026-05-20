from app.engine.portfolio_valuation import (
    get_portfolio_valuation
)

portfolio = (
    get_portfolio_valuation()
)

print("\nPORTFOLIO VALUATION:\n")

for row in portfolio:

    print(

        f"{row['symbol']} | "

        f"Qty={row['quantity']} | "

        f"AvgCost={row['average_cost']} | "

        f"Price={row['current_price']} | "

        f"Value={row['market_value']} | "

        f"UPL={row['unrealised_pl']}"
    )