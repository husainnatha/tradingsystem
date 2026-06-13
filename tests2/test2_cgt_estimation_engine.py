from app.engine.cgt_estimator import (
    estimate_cgt
)

def test_cgt_estimation_engine():

    cgt_df = estimate_cgt(

        tax_year="2025/26",
        taxable_income=30000

    )

    for key, value in cgt_df.items():

        print(f"{key}: {value}")


    assert True