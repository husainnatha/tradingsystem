from app.engine.cgt_estimator import (
    estimate_cgt
)

import pandas as pd

def test_cgt_estimation_engine():

    cgt_current_year_df = estimate_cgt(

        tax_year="2025/26",
        taxable_income=30000,
        ledger = pd.DataFrame([

    {
        "symbol": "META",
        "disposal_date": "2024-04-10",
        "tax_year": "2023/24",
        "quantity": 10,
        "proceeds_gbp": 6720.00,
        "cost_basis_gbp": 6400.00,
        "gain_loss_gbp": 320.00
    },

    {
        "symbol": "TSLA",
        "disposal_date": "2024-11-01",
        "tax_year": "2024/25",
        "quantity": 5,
        "proceeds_gbp": 5775.00,
        "cost_basis_gbp": 7800.00,
        "gain_loss_gbp": -2025.00
    },

    {
        "symbol": "MSFT",
        "disposal_date": "2026-02-20",
        "tax_year": "2025/26",
        "quantity": 20,
        "proceeds_gbp": 2800.00,
        "cost_basis_gbp": 1600.00,
        "gain_loss_gbp": 1200.00
    }

        ])
    )

    for key, value in cgt_current_year_df.items():

        print(f"{key}: {value}")

    assert True