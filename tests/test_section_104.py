from app.engine.matching_engine import (
    get_section_104_pool
)

results = get_section_104_pool()

print("\nSECTION 104 DISPOSALS:\n")

for disposal in results[
    "section_104_disposals"
]:

    print(disposal)

print("\nREMAINING SECTION 104 POOL:\n")

for symbol, data in results[
    "remaining_pool"
].items():

    print(

        f"{symbol} | "

        f"Qty={data['total_quantity']} | "

        f"Cost={data['total_cost']:.2f}"
    )