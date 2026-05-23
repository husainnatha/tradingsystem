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

    f"Sector={row['sector']} | "

    f"Bias={row['sector_bias']} | "

    f"Macro={row['macro_regime']} | "

    f"AI={row['ai_score']}"
)