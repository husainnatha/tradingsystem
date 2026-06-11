from app.engine.matching_engine import (
    get_same_day_matches,
    get_thirty_day_matches,
    get_section_104_pool
)

def test_matching_engine(
        
):

    print("\n============================")
    print(" SAME-DAY MATCHES")
    print("============================\n")

    same_day = get_same_day_matches()

    for match in same_day["matches"]:

        print(match)

    assert True

    print("\n============================")
    print(" UNMATCHED SELLS")
    print("============================\n")

    for sell in same_day[
        "unmatched_sells"
    ]:

        tx = sell["transaction"]

        print(

            f"{tx.symbol} | "

            f"SELL | "

            f"Remaining Qty="

            f"{sell['remaining_qty']}"
        )

    assert True

    print("\n============================")
    print(" THIRTY-DAY MATCHES")
    print("============================\n")

    thirty_day = (
        get_thirty_day_matches()
    )

    for match in thirty_day[
        "thirty_day_matches"
    ]:

        print(match)

    assert True

    print("\n============================")
    print(" SECTION 104 DISPOSALS")
    print("============================\n")

    s104 = get_section_104_pool()

    for disposal in s104[
        "section_104_disposals"
    ]:

        print(disposal)

    assert True

    print("\n============================")
    print(" REMAINING SECTION 104 POOL")
    print("============================\n")

    for symbol, data in s104[
        "remaining_pool"
    ].items():

        print(

            f"{symbol} | "

            f"Qty={data['total_quantity']} | "

            f"Cost={round(data['total_cost'], 2)}"
        )
    
    assert True

assert True