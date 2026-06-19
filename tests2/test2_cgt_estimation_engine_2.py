from app.engine.cgt_estimator import (
    estimate_cgt
)

def test_estimate_cgt(
    stub_ledger
):

    result = estimate_cgt(

        tax_year="2025/26",

        taxable_income=59000,

        ledger=stub_ledger
    )

    assert result["net_gain_gbp"] == 1200
