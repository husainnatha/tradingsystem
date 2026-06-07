from app.engine.portfolio_valuation import (
    get_portfolio_valuation
)

portfolio = get_portfolio_valuation()

for row in sorted(
    portfolio,
    key=lambda x: x["market_value"],
    reverse=True
):
    print(row)

print()

print(
    "TOTAL:",
    round(
        sum(
            row["market_value"]
            for row in portfolio
        ),
        2
    )
)