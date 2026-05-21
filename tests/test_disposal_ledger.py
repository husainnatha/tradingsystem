from app.engine.disposal_ledger import (
    build_disposal_ledger
)

df = build_disposal_ledger()

print("\nDISPOSAL LEDGER:\n")

for _, row in df.iterrows():

    print(

        f"{row['symbol']} | "

        f"{row['disposal_date']} | "

        f"{row['tax_year']} | "

        f"{row['rule']} | "

        f"Qty={row['quantity']} | "

        f"Proceeds=£{row['proceeds_gbp']} | "

        f"Cost=£{row['cost_basis_gbp']} | "

        f"Gain/Loss=£{row['gain_loss_gbp']}"
    )