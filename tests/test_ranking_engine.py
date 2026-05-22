from app.engine.ranking_engine import (
    build_ranked_inventory
)

df = build_ranked_inventory()

print("\nAI RANKED INVENTORY:\n")

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"AI={row['ai_score']} | "

        f"Tax={round(row['tax_efficiency_score'],2)} | "

        f"Risk={round(row['position_risk_score'],2)} | "

        f"Hold={round(row['holding_period_score'],2)} | "

        f"UPnL=£{round(row['unrealised_gain_gbp'],2)}"
    )