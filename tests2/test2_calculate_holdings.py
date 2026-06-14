from app.engine.holdings_service import(
    calculate_holdings
)
def test_calculate_holdings():

    holdings = calculate_holdings()

    for symbol, data in holdings.items():

        print(
            symbol,
            data["quantity"]
        )
    assert True