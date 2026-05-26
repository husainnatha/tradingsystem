from app.engine.rebalancing_engine import (
    build_rebalancing
)

df = build_rebalancing()

print(

    "\nREBALANCING:\n"
)

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"Current={row['current_weight']}% | "

        f"Target={row['target_weight']}% | "

        f"Diff={row['difference']}% | "

        f"{row['action']}"
    )

    print(

        f"Why: {row['reason']}\n"
    )