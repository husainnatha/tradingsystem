from src.services.capital_service import (
    CapitalService
)


def test_spreadsheet_override():

    config = (
        CapitalService
        .get_capital_config()
    )

    assert (
        config[
            "emergency_reserve"
        ]
        == 20000
    )