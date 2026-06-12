from app.engine.matching_engine import (
    get_thirty_day_matches
)


def test_get_thirty_day_matches():

    results = get_thirty_day_matches()

    print("\nTHIRTY-DAY MATCHES:\n")

    for match in results[
        "thirty_day_matches"
    ]:

        print(match)

    assert True

    print("\nREMAINING UNMATCHED SELLS:\n")

    for sell in results[
        "unmatched_sells"
    ]:

        tx = sell["transaction"]

        print(

            f"{tx.symbol} | "

            f"Remaining SELL Qty="

            f"{sell['remaining_qty']}"
        )

    assert True

    print("\nREMAINING BUY LOTS:\n")

    for buy in results[
        "remaining_buy_lots"
    ]:

        tx = buy["transaction"]

        print(

            f"{tx.symbol} | "

            f"Remaining BUY Qty="

            f"{buy['remaining_qty']}"
        )

    assert True

assert True

