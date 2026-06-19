import pytest
import pandas as pd


@pytest.fixture
def stub_ledger():

    return pd.DataFrame([

        {
            "symbol": "PANW",
            "disposal_date": "2026-02-20",
            "tax_year": "2025/26",
            "quantity": 20,
            "proceeds_gbp": 2800.00,
            "cost_basis_gbp": 1600.00,
            "gain_loss_gbp": 1200.00
        }
    ])