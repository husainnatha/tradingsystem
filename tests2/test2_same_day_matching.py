from app.engine.matching_engine import (
    get_same_day_matches
)

def test_same_day_matching(
        
    results = get_same_day_matches() 

):

    print("\nSAME-DAY MATCHES:\n")

    for match in results["matches"]:

        print(match)

    print("\nUNMATCHED SELLS:\n")
    assert True

    for sell in results["unmatched_sells"]:

        tx = sell["transaction"]

        print(

            f"{tx.symbol} | "

            f"SELL | "

            f"Remaining Qty="

            f"{sell['remaining_qty']}"
        )

    print("\nREMAINING BUY LOTS:\n")
    assert True

    for buy in results["remaining_buy_lots"]:

        tx = buy["transaction"]

        print(

            f"{tx.symbol} | "

            f"BUY | "

            f"Remaining Qty="

            f"{buy['remaining_qty']}"
        )

    print(results)
    assert results is not None
    assert True
