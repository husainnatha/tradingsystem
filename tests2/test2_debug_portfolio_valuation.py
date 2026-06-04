# tests2/test2_debug_portfolio_valuation.py

from app.engine.portfolio_valuation import (
    get_portfolio_valuation
)

def test_debug_portfolio_valuation():

    portfolio = (
        get_portfolio_valuation()
    )

    print()

    print(
        f"Rows: {len(portfolio)}"
    )

    total = 0

    for row in portfolio:

        print(
            row["symbol"],
            row["market_value"]
        )

        total += (
            row["market_value"]
        )

    print()

    print(
        f"Total: £{total:,.2f}"
    )

    assert True