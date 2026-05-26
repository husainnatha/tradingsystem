from app.engine.action_engine import (
    build_actions
)

df = build_actions()

print(

    "\nPORTFOLIO ACTIONS:\n"
)

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"{row['action']} | "

        f"Priority={row['priority']} | "

        f"£{row['value']}"
    )

    print(

        f"Why: {row['reason']}\n"
    )