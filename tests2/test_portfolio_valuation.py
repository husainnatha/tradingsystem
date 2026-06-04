from app.engine.portfolio_valuation import (
    get_portfolio_valuation
)

def test_portfolio_valuation():

    portfolio = (
        get_portfolio_valuation()
    )

    print()

    print(
        f"ROWS: {len(portfolio)}"
    )

    print()

    for row in portfolio:

        print(row)

    assert len(portfolio) > 0