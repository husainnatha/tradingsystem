from app.engine.buy_recommendation_engine import (
    build_buy_recommendations
)

from app.config.watchlist import (
    WATCHLIST
)

df = build_buy_recommendations(

    WATCHLIST
)

print("\nBUY RECOMMENDATIONS:\n")

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"AI={row['ai_score']} | "

        f"Rating={row['rating']} | "

        f"RSI={row['rsi']} | "

        f"Fit={row['portfolio_fit_score']} \n"

        f"Why: {row['explanation']}\n"
    )