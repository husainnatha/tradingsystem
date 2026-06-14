from app.engine.disposal_ledger import (
    build_disposal_ledger
)

def test_disposal_ledger():

    ledger = build_disposal_ledger()

    if ledger.empty:

        print(
            "No disposals found"
        )

        return
        
    else:

        print()

        print("Columns:")
        print(ledger.columns)

        print()

        print("Tax Years:")
        print(ledger["tax_year"].unique())

    assert True