from app.services.live_price_service import (
    get_live_price
)

symbols = [

    "NVDA",
    "TSLA",
    "META",
    "AMZN"
]

print("\nLIVE MARKET PRICES:\n")

for symbol in symbols:

    price = get_live_price(
        symbol
    )

    print(

        f"{symbol}: "
        f"${price}"
    )