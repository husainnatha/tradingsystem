from app.services.live_price_service import (
    get_live_price
)

symbols = [

    "NVDA",
    "TSLA",
    "META",
    "AMZN"
]

def test_live_prices():
    
    print("\nLIVE MARKET PRICES:\n")

    for symbol in symbols:

        price = get_live_price(
            symbol
        )

        print(

            f"{symbol}: "
            f"${price}"
        )

        assert price is not None, f"Price for {symbol} should not be None" 
        assert price > 0, f"Price for {symbol} should be greater than 0"
    