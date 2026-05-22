from app.engine.inventory_engine import (
    build_inventory_state
)

df = build_inventory_state()

print("\nINVENTORY STATE:\n")

for _, row in df.iterrows():

    print(

        f"{row['transaction_id']} | "

        f"{row['symbol']} | "

        f"Original={row['original_quantity']} | "

        f"Matched={row['matched_quantity']} | "

        f"Remaining={row['remaining_quantity']} | "

        f"Rule={row['match_rule']}"
    )