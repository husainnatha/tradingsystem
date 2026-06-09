from app.engine.cgt_estimator import (
    estimate_cgt
)

def test_cgt_estimation_engine():

    result = estimate_cgt(
        tax_year="2025/26"
    )

    print()

    for key, value in result.items():

        print(f"{key}: {value}")

    print()

    assert True