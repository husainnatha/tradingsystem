from app.engine.ranking_engine import (
    build_ranked_inventory
)

df = build_ranked_inventory()

print("\nAI RANKED INVENTORY:\n")

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"AI={row['ai_score']} | "

        f"Trend={row['bullish_trend']} | "

        f"RSI={row['rsi']} | "

        f"Momentum={row['momentum_score']} | "

        f"UPnL=£{round(row['unrealised_gain_gbp'],2)}"
    )