from app.engine.correlation_engine import (
    build_correlation_engine
)

df = build_correlation_engine()

print(
    "\nCORRELATION INTELLIGENCE:\n"
)

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"Correlation={row['avg_correlation']} | "

        f"Diversification={row['diversification_score']}"
    )