from app.services.technical_indicator_service import (
    get_technical_indicators
)

symbols = [

    "NVDA",
    "TSLA",
    "META",
    "POET"
]

print("\nTECHNICAL INDICATORS:\n")

for symbol in symbols:

    result = get_technical_indicators(
        symbol
    )

    print(result)