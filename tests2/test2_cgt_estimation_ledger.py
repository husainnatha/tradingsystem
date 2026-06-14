from app.engine.cgt_estimation_ledger import (
    build_cgt_estimation_ledger
)

def test_cgt_estimation_ledger():

    cgt_ledger_df = build_cgt_estimation_ledger()

    print(cgt_ledger_df)

    assert True