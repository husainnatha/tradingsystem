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

@pytest.fixture
def sample_stock_entry_semiconductors():
    return {
        "asset_type": "STOCK",
        "sector": "TECHNOLOGY",
        "sub_sector": "SEMICONDUCTORS",
        "themes": ["AI", "CLOUD", "SEMICONDUCTORS"],
        "innovation_score": 0.85,
        "market_cap_style": "LARGE_CAPS",
    }

@pytest.fixture
def sample_stock_entry_photonics():
    return {
        "asset_type": "STOCK",
        "sector": "TECHNOLOGY",
        "sub_sector": "PHOTONICS",
        "themes": ["PHOTONICS"],
        "innovation_score": 0.40,
        "market_cap_style": "SMALL_CAPS",
    }

@pytest.fixture
def sample_stock_entry_consumer():
    return {
        "asset_type": "STOCK",
        "sector": "CONSUMER_CYCLICAL",
        "sub_sector": "FOOTWEAR_AND_ACCESSORIES",
        "themes": ["CONSUMER"],
        "innovation_score": 0.30,
        "market_cap_style": "MID_CAPS",
    }

@pytest.fixture
def sample_metadata_file(tmp_path):
    """Creates a temporary YAML file for process_stock_metadata tests."""
    import yaml

    data = {
        "AMD": {
            "asset_type": "STOCK",
            "sector": "TECHNOLOGY",
            "sub_sector": "SEMICONDUCTORS",
            "themes": ["AI", "CLOUD", "SEMICONDUCTORS"],
            "innovation_score": 0.85,
            "market_cap_style": "LARGE_CAPS",
        },
        "LPTH": {
            "asset_type": "STOCK",
            "sector": "TECHNOLOGY",
            "sub_sector": "PHOTONICS",
            "themes": ["PHOTONICS"],
            "innovation_score": 0.40,
            "market_cap_style": "SMALL_CAPS",
        },
    }

    file_path = tmp_path / "metadata.yaml"
    with open(file_path, "w") as f:
        yaml.dump(data, f)

    return file_path
