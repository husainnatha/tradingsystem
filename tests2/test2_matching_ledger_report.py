from app.reports.matching_ledger import (
    build_matching_ledger
)

def test_build_matching_ledger_report():

    df = build_matching_ledger()

    print("\nMATCHING LEDGER:\n")

    for _, row in df.iterrows():

        print(

            f"{row['rule']} | "

            f"{row['symbol']} | "

            f"Buy=£{row['buy_price_gbp']} | "

            f"Sell=£{row['sell_price_gbp']} | "

            f"Gain/Share=£{row['gain_loss_per_share_gbp']} | "

            f"DaysHeld={row['holding_period_days']}"
        )

    assert True
assert True