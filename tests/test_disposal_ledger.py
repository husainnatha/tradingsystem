from app.engine.disposal_ledger import (
    build_disposal_ledger
)

ledger = build_disposal_ledger()

print("\nDISPOSAL LEDGER:\n")

for row in ledger:

    print(

        f"{row['symbol']} | "

        f"{row['disposal_date']} | "

        f"{row['rule']} | "

        f"Qty={row['quantity']} | "

        f"Proceeds=£{row['proceeds_gbp']} | "

        f"Cost=£{row['cost_basis_gbp']} | "

        f"Gain/Loss=£{row['gain_loss_gbp']}"
    )