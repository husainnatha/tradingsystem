from app.engine.matching_engine import (
    get_section_104_pool
)

def test_section_104_pool_disposals():

    results = get_section_104_pool()

    print("\nSECTION 104 DISPOSALS:\n")

    for disposal in results[
        "section_104_disposals"
    ]:

        print(

            f"{disposal}"
     )

    assert len(results["section_104_disposals"]) >= 0

  
def test_section_104_pool_remaining():

    results = get_section_104_pool()

    print("\nREMAINING SECTION 104 POOL:\n")

    for symbol, data in results[
        "remaining_pool"
    ].items():

        print(

            f"{symbol} | "

            f"Qty={data['total_quantity']} | "

            f"Cost={data['total_cost']:.2f}"
        )
    assert len(results["remaining_pool"]) >= 0