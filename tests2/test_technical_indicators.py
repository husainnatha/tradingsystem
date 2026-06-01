from app.services.technical_indicator_service import (
    get_technical_indicators
)

from app.config.watchlist import (
    WATCHLIST
)

print("\nTECHNICAL INDICATORS:\n")

for symbol in WATCHLIST:

    result = get_technical_indicators(
        symbol
    )

    print(result)