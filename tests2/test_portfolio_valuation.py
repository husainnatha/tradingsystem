from app.engine.portfolio_valuation import (
    get_portfolio_valuation
)

def test_portfolio_valuation():

    portfolio = (
        get_portfolio_valuation()
    )   

    assert len(portfolio) > 0

    for row in portfolio:

        assert "symbol" in row

        assert "quantity" in row

        assert "average_cost" in row

        assert "current_price" in row

        assert "market_value" in row

        assert "unrealised_pl" in row

print("\nPORTFOLIO VALUATION:\n")