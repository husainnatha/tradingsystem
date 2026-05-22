from app.engine.market_intelligence_engine import (
    build_market_intelligence
)

from app.config.watchlist import (
    WATCHLIST
)

df = build_market_intelligence(

    WATCHLIST
)

print("\nMARKET INTELLIGENCE:\n")

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"AI={row['ai_score']} | "

        f"Trend={row['bullish_trend']} | "

        f"RSI={row['rsi']} | "

        f"Rating={row['rating']}"
    )